import re
from typing import final

import sqlparse
import sqlparse.tokens as T

from app.factory.db import db_factory
from app.services.metadata_extractor import TableSchema

_SQL_KEYWORDS = {"SELECT", "INSERT", "UPDATE", "DELETE", "WITH", "CREATE", "DROP"}


@final
class SQLValidator:
    def __init__(self):
        self.engine = db_factory.get_engine()

    def _validate_syntax(self, sql: str) -> None:
        first_word = sql.strip().split()[0].upper() if sql.strip() else ""
        if first_word not in _SQL_KEYWORDS:
            raise ValueError(f"Not a valid SQL statement: {sql[:50]}")
        parsed = sqlparse.parse(sql)
        if not parsed or not parsed[0].tokens:
            raise ValueError(f"Invalid SQL syntax: {sql}")

    def _validate_semantic(self, sql: str, schema: TableSchema) -> None:
        known_tables = {t.upper(): t for t in schema}
        known_columns: dict[str, set[str]] = {
            t.upper(): {col["name"].upper() for col in cols if col["type"] != "foreign_key"}
            for t, cols in schema.items()
        }

        flat_tokens = list(sqlparse.parse(sql)[0].flatten())
        aliases: set[str] = {m.group(1).upper() for m in re.finditer(r'\bAS\s+(\w+)', sql, re.IGNORECASE)}

        names = [t.value for t in flat_tokens if t.ttype is T.Name]

        for name in names:
            upper = name.upper()
            if upper in aliases:
                continue
            if upper in known_tables:
                continue
            found_in_any_table = any(upper in cols for cols in known_columns.values())
            if not found_in_any_table:
                if upper not in {"ASC", "DESC", "NULL", "COUNT", "SUM", "AVG", "MIN", "MAX", "LIMIT"}:
                    raise ValueError(f"'{name}' does not exist in the schema")

    def validate(self, sql: str, schema: TableSchema) -> str:
        self._validate_syntax(sql)
        self._validate_semantic(sql, schema)
        return sql


validator = SQLValidator()
