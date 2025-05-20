from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

DEFAULT_PROMPT = """
                너는 전문적이고 친절한 AI 어시스턴트이다.

                사용자의 질문에 답할 때 다음과 같은 프로세스를 따른다.
                1. 질문의 의도를 파악한다.
                2. 필요한 정보를 기반으로 논리적으로 사고한다.
                3. 가능한 한 자세하고 이해하기 쉽게 설명한다.
                4. 너무 모를 경우 솔직하게 모른다고 말하되, 관련된 정보를 제공하려 노력한다.

                질문: {user_input}

                답변:
                (생각을 정리한 후, 체계적이고 논리적으로 설명하세요.)
                """

def run(user_input: str, prompt: str = DEFAULT_PROMPT) -> str:
    final_prompt = prompt.format(user_input=user_input)
    return llm.invoke(final_prompt).content
