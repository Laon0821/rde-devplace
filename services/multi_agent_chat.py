# services/multi_agent_chat.py
from agents.router_agent import route

def chat_with_agent(message_text: str):
    response = route(message_text)
    return response

if __name__ == "__main__":
    import sys
    print(chat_with_agent(sys.argv[1]))
