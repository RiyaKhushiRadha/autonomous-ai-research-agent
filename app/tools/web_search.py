from langchain_tavily import TavilySearch

from app.config.settings import settings


web_search_tool = TavilySearch(
    tavily_api_key=settings.tavily_api_key,
    max_results=5,
    topic="general",
)


def search_web(query: str):
    return web_search_tool.invoke({"query": query})