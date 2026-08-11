from fastapi import FastAPI

app = FastAPI(
    title="Autonomous AI Research Agent",
    description="Agentic AI research system using LangGraph, LangChain, RAG, tool calling, and FastAPI.",
    version="0.1.0",
)


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "Autonomous AI Research Agent",
        "version": "0.1.0",
    }