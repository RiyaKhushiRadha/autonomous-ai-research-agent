from typing import List

from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever

from app.rag.embeddings import create_query_embedding
from app.rag.vector_store import vector_store


class RetrievalServiceError(Exception):
    """Raised when document retrieval fails."""


def retrieve_documents(
    query: str,
    top_k: int = 3,
) -> list[str]:
    try:
        query_embedding = create_query_embedding(query)

        return vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k,
        )

    except Exception as exc:
        raise RetrievalServiceError(
            f"Document retrieval failed: {exc}"
        ) from exc


class DocumentRetriever(BaseRetriever):
    top_k: int = 3

    def _get_relevant_documents(self, query: str) -> List[Document]:
        results = retrieve_documents(
            query=query,
            top_k=self.top_k,
        )

        return [
            Document(page_content=result)
            for result in results
        ]