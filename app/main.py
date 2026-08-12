from fastapi import FastAPI

from app.api.routes.health import router as health_router
from app.api.routes.research import router as research_router
from app.api.routes.documents import router as documents_router

app = FastAPI(
    title="Autonomous AI Research Agent",
    description=(
        "Agentic AI research system using LangGraph, LangChain, "
        "RAG, tool calling, and FastAPI."
    ),
    version="0.1.0",
)

app.include_router(health_router)
app.include_router(research_router)
app.include_router(documents_router)