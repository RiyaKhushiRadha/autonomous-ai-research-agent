from app.agents.graph import research_graph


class ResearchService:

    async def research(self, query: str) -> dict:
        initial_state = {
            "query": query,
            "plan": [],
            "web_results": [],
            "rag_results": [],
        }

        result = research_graph.invoke(initial_state)

        verification = result.get("verification", {})

        return {
            "query": query,
            "answer": result.get("final_answer", "Research completed."),
            "verification": verification,
        }


research_service = ResearchService()