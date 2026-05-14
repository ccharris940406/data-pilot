from typing import final

from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from pydantic import SecretStr

from app.config import llm_config
from app.services.metadata_extractor import TableSchema


@final
class EmbeddingsService:
    def __init__(self):
        config = llm_config.get_llm_config()
        self._embedings = OpenAIEmbeddings(
            api_key=SecretStr(config["embedding_api_key"]),
            model=config["embedding_model"],
        )
        self._store = Chroma(
            collection_name="schema",
            embedding_function=self._embedings,
            persist_directory="data/chroma",
        )

    def index(self, schema: TableSchema) -> None:
        texts = []
        ids = []

        for table_name, columns in schema.items():
            col_str = ", ".join(f"{col['name']} ({col['type']})" for col in columns)
            texts.append(f"Table: {table_name}, Columns: {col_str}")
            ids.append(table_name)

        _ = self._store.add_texts(texts=texts, ids=ids)

    def search(self, query: str, k: int = 5) -> list[str]:
        results = self._store.similarity_search(query, k=k)
        return [doc.page_content for doc in results]

    def is_empty(self) -> bool:
        return self._store._collection.count() == 0  # pyright: ignore[reportUnknownMemberType, reportAttributeAccessIssue]


embeddings_service = EmbeddingsService()
