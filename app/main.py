from dotenv import load_dotenv

_ = load_dotenv()

from app.agents.chat import chat_agent


def main():
    print("NL2SQL Chat — type 'exit' to quit\n")
    while True:
        query = input("You: ")
        if query.lower() in ("exit", "quit"):
            break
        response = chat_agent.chat(query)
        print(f"Agent: {response}\n")


if __name__ == "__main__":
    main()
