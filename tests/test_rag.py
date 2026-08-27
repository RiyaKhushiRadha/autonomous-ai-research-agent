import pytest

from app.rag.embeddings import create_embeddings
from app.rag.retriever import retrieve_documents
from app.rag.vector_store import vector_store


@pytest.fixture(autouse=True)
def clear_vector_store():
    yield
    vector_store.documents = []
    vector_store.embeddings = []
    vector_store.document_ids = []


def test_retrieve_uploaded_document():
    documents = [
        "RAG stands for Retrieval-Augmented Generation.",
        "RAG retrieves relevant information before generating an answer.",
    ]

    embeddings = create_embeddings(documents)

    vector_store.add_documents(
        documents,
        embeddings,
        "test-document",
    )

    results = retrieve_documents(
        query="What is Retrieval-Augmented Generation?",
        top_k=2,
    )

    assert isinstance(results, list)
    assert len(results) > 0
    assert any(
        "Retrieval-Augmented Generation" in result
        for result in results
    )