from pydantic import BaseModel, Field


class ResearchRequest(BaseModel):
    query: str = Field(..., min_length=3)


class ResearchResponse(BaseModel):
    research_id: str
    query: str
    answer: str
    verification: dict