from sqlalchemy import create_engine, inspect
from sqlalchemy.engine import Engine
from typing import Optional
import pandas as pd


class DatabaseConnector:
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.engine: Optional[Engine] = None

    def connect(self) -> Engine:
        if self.engine is None:
            self.engine = create_engine(self.connection_string)
        return self.engine

    def test_connection(self) -> bool:
        try:
            engine = self.connect()
            with engine.connect() as conn:
                conn.execute("SELECT 1")
            return True
        except Exception:
            return False

    def disconnect(self):
        if self.engine:
            self.engine.dispose()
            self.engine = None

    def get_schema(self) -> dict:
        engine = self.connect()
        inspector = inspect(engine)

        tables = []
        for table_name in inspector.get_table_names():
            columns = []
            for column in inspector.get_columns(table_name):
                columns.append({
                    "name": column["name"],
                    "type": str(column["type"]),
                    "nullable": column["nullable"],
                    "default": column.get("default"),
                })

            primary_keys = inspector.get_pk_constraint(table_name)
            foreign_keys = inspector.get_foreign_keys(table_name)

            tables.append({
                "name": table_name,
                "columns": columns,
                "primary_keys": primary_keys,
                "foreign_keys": foreign_keys,
            })

        return {"tables": tables}

    def execute_query(self, query: str) -> pd.DataFrame:
        engine = self.connect()
        df = pd.read_sql_query(query, engine)
        return df


class PostgreSQLConnector(DatabaseConnector):
    def __init__(self, host: str, port: int, database: str, user: str, password: str):
        connection_string = f"postgresql://{user}:{password}@{host}:{port}/{database}"
        super().__init__(connection_string)


class MySQLConnector(DatabaseConnector):
    def __init__(self, host: str, port: int, database: str, user: str, password: str):
        connection_string = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
        super().__init__(connection_string)


class SQLiteConnector(DatabaseConnector):
    def __init__(self, database_path: str):
        connection_string = f"sqlite:///{database_path}"
        super().__init__(connection_string)