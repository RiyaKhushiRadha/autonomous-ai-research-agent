from app.agents.graph import research_graph

import pytest


@pytest.mark.asyncio
async def test_research_graph(monkeypatch):

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

    result = await research_graph.ainvoke(
        {
            "query": "What is RAG?",
            "plan": "",
            "web_results": [],
            "rag_results": [],
            "retry_count": 0,
        }
    )

    assert result["query"] == "What is RAG?"
    assert result["final_answer"]
    assert "verification" in result
    assert result["verification"]["verified"] is True