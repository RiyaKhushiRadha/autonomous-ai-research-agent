from app.agents.graph import research_graph


def test_research_graph():
    result = research_graph.invoke(
        {
            "query": "What is RAG?",
            "plan": [],
            "web_results": [],
            "rag_results": [],
        }
    )

    assert result["query"] == "What is RAG?"
    assert result["final_answer"]
    assert "verification" in result
    assert result["verification"]["verified"] is True