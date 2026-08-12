from typing import TypedDict


class ResearchState(TypedDict, total=False):
    query: str
    answer: str