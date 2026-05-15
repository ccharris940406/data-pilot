from calendar import c
from typing import final

from app.services.embeddings import embeddings_service
from app.services.metadata_extractor import TableSchema, metadata_extractor


@final
class RAGService:
    def __init__(self):
        schema = metadata_extractor.extract()
        if embeddings_service.is_empty():
            embeddings_service.index(schema)

    def retrieve(self, query: str, schema: TableSchema) -> list[str]:
        initial_result = embeddings_service.search(query)

        retrieved_tables: set[str] = set()
        for result in initial_result:
            first_line = result.split("\n")[0]
            table_name = first_line.replace("Table: ", "").split(",")[0].strip()
            retrieved_tables.add(table_name)

        context: list[str] = []
        for table in retrieved_tables:
            if table in schema:
                col_str = ", ".join(f"{c['name']} ({c['type']})" for c in schema[table])
                context.append(f"Table: {table}\nColumns: {col_str}")

        return context


rag_service = RAGService()
