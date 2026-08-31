from typing import TypedDict


class ResearchState(TypedDict):
    query: str
    document_ids: list[str] | None
    plan: str
    web_results: list[dict]
    rag_results: list[str]
    web_error: str | None
    rag_error: str | None
    verification: dict
    final_answer: str
    retry_count: int
