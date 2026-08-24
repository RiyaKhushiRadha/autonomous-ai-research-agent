from langchain_tavily import TavilySearch

from app.config.settings import settings


web_search_tool = TavilySearch(
    tavily_api_key=settings.tavily_api_key,
    max_results=5,
    topic="general",
)


def search_web(query: str) -> dict:
    """
    Execute a Tavily web search and return a controlled result.
    """
    try:
        results = web_search_tool.invoke({"query": query})

        if not isinstance(results, dict):
            return {
                "results": [],
                "error": "Web search returned an invalid response.",
            }

        return results

    except Exception as exc:
        return {
            "results": [],
            "error": f"Web search failed: {exc}",
        }