from app.agents.graph import research_graph

from app.agents.graph import MAX_RETRIES, verification_router

from app.agents.nodes import web_research_node, rag_research_node

from app.rag.retriever import RetrievalServiceError

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

def test_verification_router_stops_after_max_retries():
    state = {
        "query": "test",
        "plan": "",
        "web_results": [],
        "rag_results": [],
        "draft": "",
        "verification": {
            "verified": False,
            "reason": "Not sufficiently supported.",
        },
        "final_answer": "Best available answer.",
        "retry_count": MAX_RETRIES,
    }

    assert verification_router(state) == "end"

def test_web_research_node_preserves_error(monkeypatch):
    def mock_search_web(_):
        return {
            "results": [],
            "error": "Web search failed: Tavily unavailable",
        }

    monkeypatch.setattr(
        "app.agents.nodes.search_web",
        mock_search_web,
    )

    state = {
        "query": "What is RAG?",
        "plan": "",
        "web_results": [],
        "rag_results": [],
        "web_error": None,
        "rag_error": None,
        "draft": "",
        "verification": {},
        "final_answer": "",
        "retry_count": 0,
    }

    result = web_research_node(state)

    assert result["web_results"] == []
    assert result["web_error"] == "Web search failed: Tavily unavailable"

def test_rag_research_node_preserves_error(monkeypatch):
    def mock_retrieve_documents_tool(_):
        raise RetrievalServiceError("Vector store unavailable")

    monkeypatch.setattr(
        "app.agents.nodes.retrieve_documents_tool",
        type(
            "MockRetrievalTool",
            (),
            {
                "invoke": staticmethod(mock_retrieve_documents_tool),
            },
        )(),
    )

    state = {
        "query": "What is RAG?",
        "plan": "",
        "web_results": [],
        "rag_results": [],
        "web_error": None,
        "rag_error": None,
        "draft": "",
        "verification": {},
        "final_answer": "",
        "retry_count": 0,
    }

    result = rag_research_node(state)

    assert result["rag_results"] == []
    assert "Vector store unavailable" in result["rag_error"]

@pytest.mark.asyncio
async def test_verification_handles_invalid_json(monkeypatch):
    async def mock_generate_text(prompt):
        return "This is not valid JSON."

    monkeypatch.setattr(
        "app.agents.nodes.generate_text",
        mock_generate_text,
    )

    state = {
        "query": "What is RAG?",
        "plan": "Understand RAG.",
        "web_results": [],
        "rag_results": [],
        "web_error": None,
        "rag_error": None,
        "draft": "",
        "verification": {},
        "final_answer": "RAG retrieves relevant information and uses it to generate an answer.",
        "retry_count": 0,
    }

    from app.agents.nodes import verification_node

    result = await verification_node(state)

    assert result["verification"]["verified"] is False
    assert (
        result["verification"]["reason"]
        == "Verification response could not be parsed."
    )
    assert result["retry_count"] == 1

