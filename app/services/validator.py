from typing import final

import sqlparse

from app.factory.db import db_factory
from app.services.metadata_extractor import TableSchema


@final
class SQLValidator:
    def __init__(self):
        self.engine = db_factory.get_engine()

    def _validate_syntax(self, sql: str) -> None:
        parsed = sqlparse.parse(sql)
        if not parsed or not parsed[0].tokens:
            raise ValueError(f"Invalid SQL syntax: {sql}")

    def _validate_semantic(self, sql: str, schema: TableSchema) -> None:
        parsed = sqlparse.parse(sql)[0]
        sql_upper = sql.upper()

        for table in schema:
            if table.upper() in sql_upper:
                columns = {col["name"].upper() for col in schema[table]}
                for col in columns:
                    if col in sql_upper and col not in columns:
                        raise ValueError(
                            f"Column '{col}' does not exist in table '{table}'"
                        )

    def validate(self, sql: str, schema: TableSchema) -> str:
        self._validate_syntax(sql)
        self._validate_semantic(sql, schema)
        return sql


validator = SQLValidator()
