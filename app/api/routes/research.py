from fastapi import APIRouter, HTTPException

from app.models.research import ResearchRequest, ResearchResponse
from app.services.research_service import research_service


router = APIRouter(tags=["Research"])


@router.post(
    "/research", response_model=ResearchResponse,
    summary="Run a research query",
    description=(
        "Runs the full pipeline: plans the query, searches the web, retrieves "
        "relevant chunks from uploaded documents, generates an answer, and "
        "verifies it against the evidence."
    ),
)
async def research(request: ResearchRequest):
    result = await research_service.research(
        request.query,
        document_ids=request.document_ids,
    )

    return ResearchResponse(
        research_id=result["research_id"],
        query=result["query"],
        answer=result["answer"],
        verification=result["verification"],
    )


@router.get(
    "/research/{research_id}", response_model=ResearchResponse,
    summary="Get a past research result",
    description="Fetches a previously completed research result by ID.",
)
async def get_research(research_id: str):
    result = research_service.get_research(research_id)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Research result not found.",
        )

    return ResearchResponse(
        research_id=result["research_id"],
        query=result["query"],
        answer=result["answer"],
        verification=result["verification"],
    )
