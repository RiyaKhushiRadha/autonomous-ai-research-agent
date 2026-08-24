from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_research_endpoint(monkeypatch):

    async def mock_generate_text(prompt):
        if "research planning agent" in prompt:
            return (
                "1. Understand RAG\n"
                "2. Explain retrieval and generation\n"
                "3. Verify the explanation"
            )

        if "research verification agent" in prompt:
            return (
                '{"verified": true, '
                '"reason": "Answer is supported by the available research."}'
            )

        return (
            "RAG is Retrieval-Augmented Generation. "
            "It retrieves relevant information and uses it to generate "
            "a more accurate answer."
        )

    monkeypatch.setattr(
        "app.agents.nodes.generate_text",
        mock_generate_text
    )

    client = TestClient(app)

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


def test_get_research_by_id():
    response = client.post(
        "/research",
        json={"query": "What is RAG?"},
    )

    assert response.status_code == 200

    created = response.json()

    assert created["research_id"]

    research_id = created["research_id"]

    get_response = client.get(
        f"/research/{research_id}"
    )

    assert get_response.status_code == 200

    data = get_response.json()

    assert data["research_id"] == research_id
    assert data["query"] == "What is RAG?"
    assert isinstance(data["answer"], str)
    assert "verification" in data


def test_get_research_not_found():
    response = client.get(
        "/research/does-not-exist"
    )

    assert response.status_code == 404

    data = response.json()

    assert data["detail"] == "Research result not found."

