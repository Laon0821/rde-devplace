from agents.router_agent import route_with_trace

if __name__ == "__main__":
    while True:
        user_input = input("\n질문을 입력하세요 (종료하려면 'exit'): ")
        if user_input.lower() == "exit":
            break

        result = route_with_trace(user_input)

        print("\n=== 처리한 에이전트 ===")
        print(result["intent"])

        print("\n=== 최종 응답 ===")
        print(result["response"])

        if result.get("doc_names"):
            print("\n=== 참조 문서 (RAG 사용됨) ===")
            for doc_name in result["doc_names"]:
                print(f"- {doc_name}")
