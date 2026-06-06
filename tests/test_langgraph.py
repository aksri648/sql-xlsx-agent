import pytest
from backend.langgraph.state import AnalystState


def test_analyst_state_creation():
    state = AnalystState(
        question="Show me sales by region",
        session_id="test-session",
    )
    assert state["question"] == "Show me sales by region"
    assert state["session_id"] == "test-session"


def test_analyst_state_with_optional_fields():
    state = AnalystState(
        question="Show me sales by region",
        session_id="test-session",
        source_type="file",
        intent="aggregation",
        metrics=["sales"],
        dimensions=["region"],
    )
    assert state["source_type"] == "file"
    assert state["intent"] == "aggregation"
    assert state["metrics"] == ["sales"]
    assert state["dimensions"] == ["region"]