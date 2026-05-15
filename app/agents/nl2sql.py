from typing import final

from langchain_core.messages import BaseMessage
from langchain_core.prompts import ChatPromptTemplate

from app.config_db import db_config
from app.factory.llm import llm_factory
from app.services.executor import sql_executor
from app.services.metadata_extractor import metadata_extractor
from app.services.rag import rag_service
from app.services.validator import validator

_SYSTEM_PROMPT = """You are an expert SQL translator for {dialect}.
Given the following database schema, translate the user's question into a valid {dialect} query.
Return ONLY the SQL query, no explanations, no markdown.

Schema:
{schema}"""

_NL_PROMPT = """Given the following SQL query results, answer the user's question in natural language.

Question: {query}
Results: {results}"""

_INTENT_PROMPT = """Does the following message require a database query to answer?
Reply with only 'yes' or 'no'.

Message: {query}"""


def _clean_sql(sql: str) -> str:
    sql = sql.strip()
    if sql.startswith("```"):
        sql = sql.split("\n", 1)[-1]
    if sql.endswith("```"):
        sql = sql.rsplit("```", 1)[0]
    return sql.strip()


@final
class NL2SQLAgent:
    def __init__(self):
        self.llm = llm_factory.get_llm()
        self.schema = metadata_extractor.extract()

    def run(self, query: str) -> str:
        intent_prompt = ChatPromptTemplate.from_messages([("human", _INTENT_PROMPT)])
        intent_chain = intent_prompt | self.llm
        intent: BaseMessage = intent_chain.invoke({"query": query})

        if "no" in str(intent.content).lower():  # pyright: ignore[reportUnknownArgumentType]
            chain = ChatPromptTemplate.from_messages([("human", "{query}")]) | self.llm  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
            response: BaseMessage = chain.invoke({"query": query})  # pyright: ignore[reportUnknownMemberType]
            return str(response.content)

        context = rag_service.retrieve(query, self.schema)
        schema_str = "\n\n".join(context)

        sql_prompt = ChatPromptTemplate.from_messages(
            [("system", _SYSTEM_PROMPT), ("human", f"{query}")]
        )

        chain = sql_prompt | self.llm
        sql_response: BaseMessage = chain.invoke(
            {"schema": schema_str, "query": query, "dialect": db_config.db_type}
        )  # pyright: ignore[reportUnknownMemberType]
        sql = _clean_sql(str(sql_response.content))
        print(f"\n[SQL]: {sql}\n")

        validator.validate(sql, self.schema)
        results = sql_executor.execute(sql)

        nl_prompt = ChatPromptTemplate.from_messages([("human", _NL_PROMPT)])
        chain = nl_prompt | self.llm
        nl_response: BaseMessage = chain.invoke({"query": query, "results": results})

        return str(nl_response.content)


nl2sql_agent = NL2SQLAgent()
