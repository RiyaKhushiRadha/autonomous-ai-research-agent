import google.generativeai as genai

from app.config.settings import settings


genai.configure(api_key=settings.gemini_api_key)

model = genai.GenerativeModel("gemini-2.5-flash")


async def generate_text(prompt: str) -> str:
    response = model.generate_content(prompt)

    return response.text