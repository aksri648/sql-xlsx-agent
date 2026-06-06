import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data
    assert "services" in data


def test_chat_endpoint():
    response = client.post("/chat", json={"question": "What is sales data?"})
    assert response.status_code in [200, 500]


def test_upload_csv_invalid_file():
    response = client.post(
        "/upload/csv",
        files={"file": ("test.txt", b"test content", "text/plain")}
    )
    assert response.status_code == 400


def test_list_datasets():
    response = client.get("/datasets")
    assert response.status_code == 200
    assert "datasets" in response.json()


def test_get_nonexistent_dataset():
    response = client.get("/datasets/nonexistent-id")
    assert response.status_code == 200


def test_delete_dataset():
    response = client.delete("/datasets/test-id")
    assert response.status_code == 200
    assert response.json()["status"] == "deleted"