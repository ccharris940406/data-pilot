import json
import re
from pathlib import Path

from overrides import final

from app.services.metadata_extractor import TableSchema


def _parse_camel(name: str) -> str:
    return re.sub(r"(?<=[a-z])(?=[A-Z])", " ", name).lower()


_SYNONYMOUS: dict[str, list[str]] = {
    "invoice": ["factura", "venta", "compra", "bill"],
    "track": ["cancion", "pista", "tema", "song"],
    "artist": ["artista", "banda", "musico"],
    "album": ["album", "disco"],
    "customer": ["cliente", "comprador"],
    "employee": ["empleado", "trabajador"],
    "genre": ["genero", "estilo"],
    "playlist": ["lista", "playlist"],
    "media": ["medio", "formato"],
}


@final
class SemanticLayer:
    def __init__(self, path: str = "data/semantic_layer.json"):
        self.path = Path(path)
        self.mapping: dict[str, list[str]] = {}

    def build(self, schema: TableSchema) -> None:
        for table in schema:
            words = _parse_camel(table).split()
            synonyms: list[str] = [table.lower(), _parse_camel(table)]
            for word in words:
                synonyms += _SYNONYMOUS.get(word, [])
            self.mapping[table] = list(set(synonyms))

        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.mapping, f, ensure_ascii=False, indent=2)

    def load(self) -> None:
        if not self.path.exists():
            raise FileNotFoundError(f"Semantic layer file not found: {self.path}")
        with open(self.path, "r", encoding="utf-8") as f:
            self.mapping = json.load(f)

    def enrich(self, query: str) -> str:
        enriched = query
        for table, synonyms in self.mapping.items():
            for synonym in synonyms:
                if synonym in query.lower():
                    enriched += f" [{table}]"

        return enriched


semantic_layer = SemanticLayer()
