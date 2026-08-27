from langchain_google_genai import ChatGoogleGenerativeAI

from app.config.settings import settings


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=settings.gemini_api_key,
)


class LLMServiceError(Exception):
    """Raised when the LLM service fails."""


async def generate_text(prompt: str) -> str:
    try:
        response = await llm.ainvoke(prompt)
    except Exception as exc:
        raise LLMServiceError(f"LLM service failed: {exc}") from exc

    if not response or not response.content:
        raise LLMServiceError("LLM returned an empty response.")

    return response.content