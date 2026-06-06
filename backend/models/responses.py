from pydantic import BaseModel, Field
from typing import Any, Optional


class ChartConfig(BaseModel):
    chart_type: str = Field(..., description="Type of chart to render")
    x_axis: str = Field(..., description="X-axis field")
    y_axis: str = Field(..., description="Y-axis field")
    title: Optional[str] = None


class ChatResponse(BaseModel):
    answer: str = Field(..., description="Natural language answer")
    insights: list[str] = Field(default_factory=list, description="Key insights")
    chart: Optional[ChartConfig] = None
    generated_sql: Optional[str] = None
    generated_pandas: Optional[str] = None
    sources: list[str] = Field(default_factory=list, description="External sources")
    follow_up_questions: list[str] = Field(default_factory=list)
    session_id: str = Field(..., description="Session ID for conversation continuity")


class DatasetResponse(BaseModel):
    id: str
    name: str
    source_type: str
    row_count: int
    column_count: int
    columns: list[dict[str, Any]]
    created_at: str


class SchemaResponse(BaseModel):
    tables: list[dict[str, Any]]
    relationships: list[dict[str, Any]]
    database_name: Optional[str] = None


class HealthResponse(BaseModel):
    status: str
    version: str
    services: dict[str, bool]