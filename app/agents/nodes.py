from app.agents.state import ResearchState


async def research_node(state: ResearchState) -> ResearchState:
    query = state.get("query", "")

    return {
        **state,
        "answer": f"Research workflow not implemented yet for: {query}",
    }