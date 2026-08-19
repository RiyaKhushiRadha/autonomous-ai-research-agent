from langchain_google_genai import ChatGoogleGenerativeAI

from app.config.settings import settings


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=settings.gemini_api_key,
)


async def generate_text(prompt: str) -> str:
    response = await llm.ainvoke(prompt)

    return response.content