from langchain_google_genai import GoogleGenerativeAIEmbeddings

from app.config.settings import settings

from sentence_transformers import SentenceTransformer

_embeddings_model = SentenceTransformer("all-MiniLM-L6-v2")


def create_embeddings(texts: list[str]) -> list[list[float]]:
    return _embeddings_model.encode(texts).tolist()


def create_query_embedding(query: str) -> list[float]:
    return _embeddings_model.encode(query).tolist()