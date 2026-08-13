from typing import TypedDict


class ResearchState(TypedDict):
    query: str
    plan: str
    web_results: list[dict]
    rag_results: list[str]
    draft: str
    verification: str
    final_answer: str