from typing import final

from sqlalchemy import text

from app.factory.db import db_factory


@final
class SQLExecutor:
    def __init__(self):
        self.engine = db_factory.get_engine()

    def execute(self, sql: str) -> list[dict[str, object]]:
        with self.engine.connect() as conn:
            result = conn.execute(text(sql))
            columns = list(result.keys())
            return [dict(zip(columns, row)) for row in result.fetchall()]


sql_executor = SQLExecutor()
