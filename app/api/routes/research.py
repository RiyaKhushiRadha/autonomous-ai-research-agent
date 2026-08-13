from fastapi import APIRouter

from app.models.research import ResearchRequest, ResearchResponse
from app.services.research_service import research_service


router = APIRouter()


@router.post("/research", response_model=ResearchResponse)
async def research(request: ResearchRequest):
    result = await research_service.research(request.query)

    return ResearchResponse(
        query=request.query,
        answer=result["answer"],
        verification=result["verification"],
    )