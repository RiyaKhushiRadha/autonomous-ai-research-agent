from app.tools import web_search
from app.rag import retriever

def test_web_search_handles_failure(monkeypatch):
    def mock_invoke(*args, **kwargs):
        raise Exception("Tavily unavailable")

    monkeypatch.setattr(
        web_search.TavilySearch,
        "invoke",
        mock_invoke,
    )

    result = web_search.search_web("What is RAG?")

    assert result["results"] == []
    assert "Web search failed" in result["error"]

def test_document_retrieval_handles_failure(monkeypatch):
    def mock_embedding(_):
        raise Exception("Embedding service unavailable")

    monkeypatch.setattr(
        retriever,
        "create_query_embedding",
        mock_embedding,
    )

    try:
        retriever.retrieve_documents("What is RAG?")
        assert False, "Expected RetrievalServiceError"
    except retriever.RetrievalServiceError as exc:
        assert "Document retrieval failed" in str(exc)