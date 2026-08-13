import numpy as np


class VectorStore:
    def __init__(self):
        self.documents = []
        self.embeddings = []

    def add_documents(
        self,
        documents: list[str],
        embeddings: list[list[float]],
    ) -> None:
        self.documents.extend(documents)
        self.embeddings.extend(embeddings)

    def search(
        self,
        query_embedding: list[float],
        top_k: int = 3,
    ) -> list[str]:
        if not self.documents:
            return []

        query_vector = np.array(query_embedding)

        document_vectors = np.array(self.embeddings)

        scores = document_vectors @ query_vector

        top_indices = np.argsort(scores)[::-1][:top_k]

        return [self.documents[index] for index in top_indices]


vector_store = VectorStore()