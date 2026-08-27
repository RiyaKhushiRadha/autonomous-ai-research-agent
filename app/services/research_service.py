import uuid

from app.agents.graph import research_graph, MAX_RETRIES
from app.rag.retriever import RetrievalServiceError
from app.services.llm_service import LLMServiceError


class ResearchService:

    def __init__(self):
        self.research_results = {}

    async def research(self, query: str) -> dict:
        research_id = str(uuid.uuid4())

        initial_state = {
            "query": query,
            "plan": "",
            "web_results": [],
            "rag_results": [],
            "web_error": None,
            "rag_error": None,
            "draft": "",
            "verification": {},
            "final_answer": "",
            "retry_count": 0,
        }

        try:
            result = await research_graph.ainvoke(initial_state)

        except (LLMServiceError, RetrievalServiceError) as exc:
            research_result = {
                "research_id": research_id,
                "query": query,
                "answer": (
                    "The research could not be completed because "
                    "a required AI service or document retrieval service "
                    "is currently unavailable."
                ),
                "verification": {
                    "verified": False,
                    "reason": str(exc),
                },
            }

            self.research_results[research_id] = research_result

            return research_result

        verification = result.get("verification", {})
        retry_count = result.get("retry_count", 0)

        if (
            verification.get("verified") is False
            and retry_count >= MAX_RETRIES
        ):
            verification = {
                **verification,
                "reason": (
                    verification.get("reason", "")
                    + " Maximum verification retries reached; "
                    "returning the best available answer."
                ).strip(),
            }

        research_result = {
            "research_id": research_id,
            "query": query,
            "answer": result.get(
                "final_answer",
                "Research completed.",
            ),
            "verification": verification,
        }

        self.research_results[research_id] = research_result

        return research_result

    def get_research(self, research_id: str) -> dict | None:
        return self.research_results.get(research_id)


research_service = ResearchService()