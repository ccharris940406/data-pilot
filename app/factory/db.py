from typing import final

from sqlalchemy import Engine, create_engine

from app.config_db import db_config


@final
class DBFactory:
    def get_engine(self) -> Engine:
        db_type = db_config.db_type

        if db_type == "sqlite":
            if not db_config.db_path:
                raise ValueError("DB_PATH is required for sqlite")
            return create_engine(f"sqlite:///{db_config.db_path}")

        if db_type in ("postgresql", "mysql"):
            if not db_config.db_uri:
                raise ValueError(f"DB_URI is required for {db_type}")
            return create_engine(db_config.db_uri)

        if db_type == "cosmosdb":
            if not db_config.db_uri:
                raise ValueError("DB_URI is required for CosmosDB")
            raise NotImplementedError("CosmosDB support is not implemented yet")

        raise ValueError(f"Unsupported DB_TYPE: {db_type}")


db_factory = DBFactory()
