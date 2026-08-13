from app.rag.retriever import retrieve_documents
from app.rag.vector_store import vector_store


def test_retrieve_uploaded_document():
    # This test expects the document to already be indexed
    # in the in-memory vector store.

    if not vector_store.documents:
        return

    query = "What is the main topic of this document?"

    results = retrieve_documents(
        query=query,
        top_k=3,
    )

    assert isinstance(results, list)
    assert len(results) > 0