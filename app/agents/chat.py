from typing import final

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage

from app.agents.nl2sql import nl2sql_agent


@final
class ChatAgent:
    def __init__(self):
        self.history: list[BaseMessage] = []

    def chat(self, query: str) -> str:
        self.history.append(HumanMessage(content=query))

        context = "\n".join(
            f"{'User' if isinstance(m, HumanMessage) else 'Assistant'}: {m.content}"
            for m in self.history[:-1]
        )

        full_query = f"{context}\nUser: {query}" if context else query
        response = nl2sql_agent.run(full_query)

        self.history.append(AIMessage(content=response))
        return response


chat_agent = ChatAgent()
