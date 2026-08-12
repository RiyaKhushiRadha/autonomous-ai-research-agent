from pydantic import BaseModel, Field


class ResearchRequest(BaseModel):
    query: str = Field(..., min_length=3)


class ResearchResponse(BaseModel):
    query: str
    answer: str