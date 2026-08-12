from app.agents.nodes import research_node
from app.agents.state import ResearchState


class ResearchGraph:

    async def run(self, query: str) -> str:
        state: ResearchState = {
            "query": query,
        }

        result = await research_node(state)

        return result["answer"]


research_graph = ResearchGraph()