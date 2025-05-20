from utils.api_client import CompanyAPIClient
from langchain_openai import ChatOpenAI

api_client = CompanyAPIClient()
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

DEFAULT_PROMPT = """
                너는 회사 업무 프로세스와 문서 양식에 정통한 전문가이다.

                사용자 질문:
                {user_input}

                답변을 제공할 때 다음 절차를 따른다.
                1. 사용자 질문과 일치하는 Template이 있는지 확인한다.
                2. Template이 있다면 그대로 친절하게 전달한다.
                3. Template이 없다면, 일반적인 업무 가이드라인과 예시를 제공하여 최대한 도움을 준다.

                답변:
                (상황에 맞게 Template 또는 가이드라인을 논리적으로 설명하세요.)
                """

def run(user_input: str, prompt: str = DEFAULT_PROMPT) -> str:
    template = api_client.search_templates(user_input)
    if template:
        return f"Template 추천:\n\n{template}"
    
    final_prompt = prompt.format(user_input=user_input)
    return llm.invoke(final_prompt).content
