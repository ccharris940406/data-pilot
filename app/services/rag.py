from typing import final

from app.services.embeddings import embeddings_service
from app.services.metadata_extractor import metadata_extractor


@final
class RAGService:
    def __init__(self):
        schema = metadata_extractor.extract()
        if embeddings_service.is_empty():
            embeddings_service.index(schema)

    def retrieve(self, query: str) -> list[str]:
        return embeddings_service.search(query)


rag_service = RAGService()
