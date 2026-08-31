from io import BytesIO

from fastapi.testclient import TestClient

from app.main import app
from app.rag.retriever import retrieve_documents
from app.rag.vector_store import vector_store


client = TestClient(app)


def test_uploaded_document_can_be_retrieved():
    file_content = b"""
    Retrieval-Augmented Generation (RAG) combines document retrieval
    with language model generation. It retrieves relevant information
    from documents before generating an answer.
    """

    response = client.post(
        "/documents/upload",
        files={
            "file": (
                "rag_test.txt",
                BytesIO(file_content),
                "text/plain",
            )
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["document_id"]
    assert data["filename"] == "rag_test.txt"

    results = retrieve_documents(
        query="What does RAG combine?",
        top_k=3,
    )

    assert isinstance(results, list)
    assert len(results) > 0

    assert any(
        "document retrieval" in result.lower()
        or "language model generation" in result.lower()
        for result in results
    )

    document_id = data["document_id"]

    deleted = vector_store.delete_document(document_id)

    assert deleted is True