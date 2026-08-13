from sentence_transformers import SentenceTransformer


_model = SentenceTransformer("all-MiniLM-L6-v2")


def create_embeddings(texts: list[str]) -> list[list[float]]:
    embeddings = _model.encode(
        texts,
        normalize_embeddings=True,
    )

    return embeddings.tolist()


def create_query_embedding(query: str) -> list[float]:
    embedding = _model.encode(
        [query],
        normalize_embeddings=True,
    )

    return embedding[0].tolist()