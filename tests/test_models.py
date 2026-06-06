import pytest
from backend.models.requests import ChatRequest, DatabaseConnectRequest
from backend.models.responses import ChatResponse, HealthResponse, ChartConfig


def test_chat_request():
    request = ChatRequest(question="What is sales?")
    assert request.question == "What is sales?"
    assert request.session_id is None


def test_chat_request_with_session():
    request = ChatRequest(question="What is sales?", session_id="abc123")
    assert request.session_id == "abc123"


def test_database_connect_request():
    request = DatabaseConnectRequest(
        connection_type="postgresql",
        connection_string="localhost:5432/mydb",
        alias="My DB"
    )
    assert request.connection_type == "postgresql"
    assert request.connection_string == "localhost:5432/mydb"
    assert request.alias == "My DB"


def test_health_response():
    response = HealthResponse(
        status="healthy",
        version="0.1.0",
        services={"groq": True, "chroma": True}
    )
    assert response.status == "healthy"
    assert response.version == "0.1.0"
    assert response.services["groq"] is True


def test_chart_config():
    config = ChartConfig(
        chart_type="bar",
        x_axis="region",
        y_axis="sales"
    )
    assert config.chart_type == "bar"
    assert config.x_axis == "region"
    assert config.y_axis == "sales"