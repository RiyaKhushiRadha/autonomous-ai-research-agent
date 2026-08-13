from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_research_endpoint():
    response = client.post(
        "/research",
        json={"query": "What is RAG?"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["query"] == "What is RAG?"
    assert isinstance(data["answer"], str)
    assert len(data["answer"]) > 0
    assert "verification" in data
    assert data["verification"]["verified"] is True