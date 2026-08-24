import numpy as np


class VectorStore:
    def __init__(self):
        self.documents = []
        self.embeddings = []
        self.document_ids = []

    def add_documents(
        self,
        documents: list[str],
        embeddings: list[list[float]],
        document_id: str,
    ) -> None:
        self.documents.extend(documents)
        self.embeddings.extend(embeddings)
        self.document_ids.extend([document_id] * len(documents))

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

    def delete_document(self, document_id: str) -> bool:
        keep_indices = [
            index
            for index, stored_id in enumerate(self.document_ids)
            if stored_id != document_id
        ]

        if len(keep_indices) == len(self.documents):
            return False

        self.documents = [
            self.documents[index]
            for index in keep_indices
        ]

        self.embeddings = [
            self.embeddings[index]
            for index in keep_indices
        ]

        self.document_ids = [
            self.document_ids[index]
            for index in keep_indices
        ]

        return True


vector_store = VectorStore()