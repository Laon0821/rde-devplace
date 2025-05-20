from langchain_openai import ChatOpenAI
from utils.vectordb.retriever import search

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

DEFAULT_PROMPT = """
                너는 회사 공간 정보와 관련된 전문가이다. 다음 사옥 문서를 참고하여 사용자의 질문에 상세하게 답하라.

                사옥 문서:
                {context}

                사용자 질문:
                {user_input}

                답변을 제공할 때 다음 절차를 따른다.
                1. 문서에서 관련된 공간 정보를 찾는다.
                2. 정보를 바탕으로 사용자의 질문에 정확하고 친절하게 설명한다.
                3. 가능하면 절차나 이용 방법까지 포함하여 안내한다.

                답변:
                (친절하고 상세한 설명을 통해 사용자가 쉽게 이해할 수 있도록 작성하세요.)
                """
                
def run(user_input: str, prompt: str = DEFAULT_PROMPT) -> str:
    docs = search("space", user_input, k=3)
    context = "\n".join([d.page_content for d in docs])
    final_prompt = prompt.format(context=context, user_input=user_input)
    return llm.invoke(final_prompt).content

def search_docs(user_input: str):
    return search("space", user_input, k=3)
