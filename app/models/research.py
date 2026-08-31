from pydantic import BaseModel, Field


class ResearchRequest(BaseModel):
    query: str = Field(
        ...,
        min_length=3,
        description=(
            "The question to research. The agent searches the web and, if "
            "documents have been uploaded, also retrieves relevant context "
            "from them."
        ),
        examples=["What are the latest advances in retrieval-augmented generation?"],
    )
    document_ids: list[str] | None = Field(
        default=None,
        description=(
            "Optional list of uploaded document IDs to restrict retrieval to. "
            "When omitted, all uploaded documents are eligible for retrieval."
        ),
    )


class ResearchResponse(BaseModel):
    research_id: str
    query: str
    answer: str
    verification: dict
