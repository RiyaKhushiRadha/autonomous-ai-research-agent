from fastapi import APIRouter

router = APIRouter(tags=["Health"])

@router.get(
    "/health",
    summary="Health check",
    description="Simple liveness check for the API.",
)
async def health_check():
    return {
        "status": "healthy",
        "service": "Autonomous AI Research Agent",
        "version": "0.1.0",
    }