from fastapi import APIRouter, HTTPException

from app.models.research import ResearchRequest, ResearchResponse
from app.services.research_service import research_service


router = APIRouter()


@router.post("/research", response_model=ResearchResponse)
async def research(request: ResearchRequest):
    result = await research_service.research(request.query)

    return ResearchResponse(
        research_id=result["research_id"],
        query=result["query"],
        answer=result["answer"],
        verification=result["verification"],
    )


@router.get("/research/{research_id}", response_model=ResearchResponse)
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