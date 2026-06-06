from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from backend.models.requests import DatabaseConnectRequest
from backend.connectors.postgresql_connector import PostgreSQLConnector
from backend.connectors.mysql_connector import MySQLConnector
from backend.connectors.sqlite_connector import SQLiteConnector
from backend.vectorstore.chroma_manager import ChromaManager

router = APIRouter(prefix="/database", tags=["database"])
chroma_manager = ChromaManager()


@router.post("/connect")
async def connect_database(request: DatabaseConnectRequest):
    try:
        if request.connection_type == "postgresql":
            connector = PostgreSQLConnector(
                host="localhost",
                port=5432,
                database=request.connection_string,
                user="user",
                password="password",
            )
        elif request.connection_type == "mysql":
            connector = MySQLConnector(
                host="localhost",
                port=3306,
                database=request.connection_string,
                user="user",
                password="password",
            )
        elif request.connection_type == "sqlite":
            connector = SQLiteConnector(database_path=request.connection_string)
        else:
            raise HTTPException(status_code=400, detail="Unsupported database type")

        if not connector.test_connection():
            raise HTTPException(status_code=400, detail="Connection failed")

        schema = connector.get_schema()

        chroma_manager.add_schema(
            schema_data=schema,
            metadata={
                "id": request.connection_string,
                "name": request.alias or request.connection_type,
                "type": "database",
            }
        )

        return JSONResponse({
            "status": "connected",
            "alias": request.alias or request.connection_type,
            "schema": schema,
        })

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))