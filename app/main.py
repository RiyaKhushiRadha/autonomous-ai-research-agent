from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api.routes.health import router as health_router
from app.api.routes.research import router as research_router
from app.api.routes.documents import router as documents_router

app = FastAPI(
    title="Autonomous AI Research Agent",
    description=(
        "An agentic AI research system built with LangGraph, LangChain, RAG, "
        "and tool calling.\n\n"
        "Ask any question — the agent plans the query, searches the web, "
        "retrieves relevant context from any uploaded documents, and returns "
        "a verified answer."
    ),
    version="0.1.0",
)

static_directory = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=static_directory), name="static")


@app.get("/", include_in_schema=False)
async def home() -> FileResponse:
    return FileResponse(static_directory / "index.html")

app.include_router(health_router)
app.include_router(research_router)
app.include_router(documents_router)
