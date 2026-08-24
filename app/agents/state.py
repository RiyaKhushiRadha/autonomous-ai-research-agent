from typing import TypedDict


class ResearchState(TypedDict):
    query: str
    plan: str
    web_results: list[dict]
    rag_results: list[str]
    web_error: str | None
    rag_error: str | None
    draft: str
    verification: dict
    final_answer: str
    retry_count: int