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
        document_ids: list[str] | None = None,
    ) -> list[str]:
        if not self.documents:
            return []

        query_vector = np.array(query_embedding)

        document_vectors = np.array(self.embeddings)

        if document_ids is None:
            eligible_indices = list(range(len(self.documents)))
        else:
            requested_ids = set(document_ids)
            eligible_indices = [
                index
                for index, stored_id in enumerate(self.document_ids)
                if stored_id in requested_ids
            ]

        if not eligible_indices:
            return []

        scores = document_vectors[eligible_indices] @ query_vector

        ranked_indices = np.argsort(scores)[::-1][:top_k]

        return [
            self.documents[eligible_indices[index]]
            for index in ranked_indices
        ]

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
