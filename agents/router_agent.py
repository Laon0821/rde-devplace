from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END, START
from typing import TypedDict, Optional, Literal
from pathlib import Path
from agents import regulation_agent, space_agent, worker_agent, general_agent

# ----------------------------
# 상태 정의 (입력 → 분류 → 응답)
# ----------------------------

class AgentState(TypedDict):
    user_input: str
    intent: Optional[Literal["regulation", "space", "worker", "general"]]
    response: Optional[str]
    next_node: Optional[str]

# ----------------------------
# 에이전트 매핑
# ----------------------------

AGENT_MAP = {
    "regulation": regulation_agent.run,
    "space": space_agent.run,
    "worker": worker_agent.run,
    "general": general_agent.run,
}

# ----------------------------
# LLM (GPT-4o-mini 사용)
# ----------------------------

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# ----------------------------
# Supervisor Agent (Intent 분류)
# ----------------------------

def supervisor_agent(state: AgentState) -> AgentState:
    user_input = state["user_input"]

    system_prompt = """
                    너는 사용자의 질문을 다음 4개 카테고리(Intent) 중 하나로만 정확하게 분류하는 에이전트이다.

                    Intent 목록:
                    - regulation: 회사 내규, 법률, 인사, 근태, 연차, 휴가, 경조사 등 규정 관련 질문
                    - space: 사옥, 조직도, 연락처, 좌석, 위치, 시설, 회의실 등 공간 관련 질문
                    - worker: 업무 처리 방법, 업무 양식, 템플릿 등 프로세스 관련 질문
                    - general: 위에 해당하지 않는 일반적인 질문 (예: 날씨, 일상 대화 등)

                    규칙:
                    - 반드시 위 4개 중 하나만 소문자로 정확히 선택할 것
                    - 다른 단어나 조합 사용 금지

                    질문: {input}
                    답변 (intent 중 하나만):
                    """

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}")
    ])

    chain = prompt | llm | (lambda x: x.content.strip().lower())
    intent = chain.invoke({"input": user_input})

    return {
        **state,
        "intent": intent,
        "next_node": intent
    }

# ----------------------------
# 공통 Agent Executor
# ----------------------------

def common_agent_executor(state: AgentState) -> AgentState:
    agent_name = state["next_node"]
    user_input = state["user_input"]

    agent = AGENT_MAP.get(agent_name)

    if agent is None:
        result = "적절한 에이전트가 없습니다."
    else:
        result = agent(user_input)

    return {**state, "response": result}

# ----------------------------
# LangGraph 구성
# ----------------------------

graph = StateGraph(AgentState)

graph.add_node("supervisor", supervisor_agent)
graph.add_node("agent_executor", common_agent_executor)

graph.add_edge(START, "supervisor")

graph.add_conditional_edges("supervisor", lambda state: state["next_node"], {
    "regulation": "agent_executor",
    "space": "agent_executor",
    "worker": "agent_executor",
    "general": "agent_executor",
})

graph.add_edge("agent_executor", END)

runnable = graph.compile()

# ----------------------------
# 외부 호출용 실행 함수
# ----------------------------

def route(user_input: str) -> str:
    result = runnable.invoke({"user_input": user_input})
    return result["response"]

# 통합 테스트용 확장 함수
def route_with_trace(user_input: str) -> dict:
    # 원래 route() 호출
    result = runnable.invoke({"user_input": user_input})

    # intent 정보만 추출
    intent = result.get("intent")
    response = result.get("response")

    # RAG 기반인지 판별 (regulation, space 만 해당)
    doc_names = None
    if intent == "regulation":
        from agents import regulation_agent
        docs = regulation_agent.search_docs(user_input)
        doc_names = sorted({Path(doc.metadata.get("source", "unknown")).name for doc in docs})
    elif intent == "space":
        from agents import space_agent
        docs = space_agent.search_docs(user_input)
        doc_names = sorted({Path(doc.metadata.get("source", "unknown")).name for doc in docs})

    return {
        "intent": intent,
        "response": response,
        "doc_names": doc_names
    }
