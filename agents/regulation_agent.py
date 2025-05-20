from langchain_openai import ChatOpenAI
from utils.vectordb.retriever import search

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

DEFAULT_PROMPT = """
                너는 회사 내규와 법률에 정통한 전문가이다. 다음 문서를 참고하여 사용자의 질문에 정확히 답변하라.

                내규 문서:
                {context}

                사용자 질문:
                {user_input}

                답변을 제공할 때 다음 절차를 따른다.
                1. 문서에서 관련 규정을 찾는다.
                2. 관련 규정을 바탕으로 사용자 질문에 적합한 내용을 정리한다.
                3. 규정 기반의 답변임을 명확히 하고, 필요하면 사례나 예시를 통해 설명한다.

                답변:
                (충분한 근거와 논리를 통해 명확하고 정확하게 작성하세요.)
                """

def run(user_input: str, prompt: str = DEFAULT_PROMPT) -> str:
    docs = search("regulation", user_input, k=3)
    context = "\n".join([d.page_content for d in docs])
    final_prompt = prompt.format(context=context, user_input=user_input)
    return llm.invoke(final_prompt).content

def search_docs(user_input: str):
    return search("regulation", user_input, k=3)
