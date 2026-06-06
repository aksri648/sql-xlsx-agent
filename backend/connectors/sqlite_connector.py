from sqlalchemy import create_engine, inspect
from sqlalchemy.engine import Engine
from typing import Optional
import pandas as pd


class SQLiteConnector:
    def __init__(self, database_path: str):
        self.connection_string = f"sqlite:///{database_path}"
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
                })

            tables.append({
                "name": table_name,
                "columns": columns,
            })

        return {"tables": tables}

    def execute_query(self, query: str) -> pd.DataFrame:
        engine = self.connect()
        df = pd.read_sql_query(query, engine)
        return df