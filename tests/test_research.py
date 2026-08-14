from fastapi.testclient import TestClient

from app.main import app


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