from typing import final

from dotenv import load_dotenv
from sqlalchemy import inspect
from sqlalchemy.util.typing import TypeAlias

from app.factory.db import db_factory

_ = load_dotenv()

TableSchema: TypeAlias = dict[str, list[dict[str, str]]]


@final
class MetadataExtractor:
    def __init__(self):
        self.engine = db_factory.get_engine()

    def extract(self) -> TableSchema:
        inspector = inspect(self.engine)
        schema: TableSchema = {}

        for table_name in inspector.get_table_names():
            columns: list[dict[str, str]] = []

            for col in inspector.get_columns(table_name):
                columns.append({"name": col["name"], "type": str(col["type"])})

            for fk in inspector.get_foreign_keys(table_name):
                columns.append(
                    {
                        "name": f"FK: {fk['constrained_columns']} -> {fk['referred_table']}.{fk['referred_columns']}",
                        "type": "foreign_key",
                    }
                )

            schema[table_name] = columns

        return schema


metadata_extractor = MetadataExtractor()
