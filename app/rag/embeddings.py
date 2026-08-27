from langchain_google_genai import GoogleGenerativeAIEmbeddings

from app.config.settings import settings


_embeddings_model = GoogleGenerativeAIEmbeddings(
    model="models/text-embedding-004",
    google_api_key=settings.gemini_api_key,
)


def create_embeddings(texts: list[str]) -> list[list[float]]:
    return _embeddings_model.embed_documents(texts)


def create_query_embedding(query: str) -> list[float]:
    return _embeddings_model.embed_query(query)