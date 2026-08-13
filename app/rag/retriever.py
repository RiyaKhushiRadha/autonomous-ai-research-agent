from app.rag.embeddings import create_query_embedding
from app.rag.vector_store import vector_store


def retrieve_documents(
    query: str,
    top_k: int = 3,
) -> list[str]:
    query_embedding = create_query_embedding(query)

    return vector_store.search(
        query_embedding=query_embedding,
        top_k=top_k,
    )