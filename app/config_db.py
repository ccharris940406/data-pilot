from os import getenv
from typing import final


@final
class DBConfig:
    def __init__(self):
        self.db_type = getenv("DB_TYPE", "sqlite").lower()
        self.db_path = getenv("DB_PATH")
        self.db_uri = getenv("DB_URI")


db_config = DBConfig()
