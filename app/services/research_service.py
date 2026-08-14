from app.agents.graph import research_graph


class ResearchService:

    async def research(self, query: str) -> dict:
        initial_state = {
            "query": query,
            "plan": "",
            "web_results": [],
            "rag_results": [],
            "draft": "",
            "verification": {},
            "final_answer": "",
            "retry_count": 0,
        }

        result = await research_graph.ainvoke(initial_state)

        verification = result.get("verification", {})

        return {
            "query": query,
            "answer": result.get("final_answer", "Research completed."),
            "verification": verification,
        }


research_service = ResearchService()