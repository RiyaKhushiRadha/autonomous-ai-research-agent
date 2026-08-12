from app.agents.graph import research_graph


class ResearchService:

    async def research(self, query: str) -> str:
        return await research_graph.run(query)


research_service = ResearchService()