from typing import TypedDict, NotRequired
from typing import Any


class AnalystState(TypedDict):
    question: str
    session_id: str
    source_type: NotRequired[str]
    schema_context: NotRequired[dict[str, Any]]
    retrieved_context: NotRequired[list[dict[str, Any]]]
    analysis_plan: NotRequired[list[str]]
    generated_sql: NotRequired[str]
    generated_pandas: NotRequired[str]
    results: NotRequired[dict[str, Any]]
    tavily_context: NotRequired[list[dict[str, Any]]]
    external_sources: NotRequired[list[str]]
    insights: NotRequired[dict[str, Any]]
    visualization: NotRequired[dict[str, Any]]
    response: NotRequired[dict[str, Any]]
    error: NotRequired[str]
    needs_external_research: NotRequired[bool]
    intent: NotRequired[str]
    metrics: NotRequired[list[str]]
    dimensions: NotRequired[list[str]]
    filters: NotRequired[list[dict[str, Any]]]
    date_range: NotRequired[str]