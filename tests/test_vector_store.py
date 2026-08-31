from app.rag.vector_store import VectorStore


def test_search_can_be_limited_to_requested_uploaded_documents():
    store = VectorStore()
    store.add_documents(
        ["Document one evidence"],
        [[1.0, 0.0]],
        "document-one",
    )
    store.add_documents(
        ["Document two evidence"],
        [[0.0, 1.0]],
        "document-two",
    )

    results = store.search(
        query_embedding=[0.0, 1.0],
        document_ids=["document-one"],
    )

    assert results == ["Document one evidence"]
