from pydantic import BaseModel, Field
from typing import Optional


class ChatRequest(BaseModel):
    question: str = Field(..., description="User's question in natural language")
    session_id: Optional[str] = Field(None, description="Conversation session ID")
    dataset_id: Optional[str] = Field(None, description="Specific dataset to query")
    database_id: Optional[str] = Field(None, description="Specific database to query")


class CSVUploadRequest(BaseModel):
    file_path: str
    dataset_name: str = Field(..., description="Name for the uploaded dataset")


class ExcelUploadRequest(BaseModel):
    file_path: str
    dataset_name: str = Field(..., description="Name for the uploaded dataset")
    sheet_name: Optional[str] = Field(None, description="Specific sheet to load")


class DatabaseConnectRequest(BaseModel):
    connection_type: str = Field(..., description="postgresql, mysql, sqlite, sqlserver")
    connection_string: str = Field(..., description="Database connection string")
    alias: Optional[str] = Field(None, description="Friendly name for the connection")