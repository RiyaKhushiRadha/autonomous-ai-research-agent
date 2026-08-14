from langgraph.graph import END, START, StateGraph

from app.agents.nodes import (
    planner_node,
    web_research_node,
    rag_research_node,
    research_node,
    verification_node,
)

from app.agents.state import ResearchState


workflow = StateGraph(ResearchState)


workflow.add_node("planner", planner_node)
workflow.add_node("web_research", web_research_node)
workflow.add_node("rag_research", rag_research_node)
workflow.add_node("research", research_node)
workflow.add_node("verification", verification_node)


def verification_router(state: ResearchState) -> str:
    verification = state.get("verification", {})
    retry_count = state.get("retry_count", 0)

    if verification.get("verified") is True:
        return "end"

    if retry_count < 2:
        return "retry"

    return "end"


workflow.add_edge(START, "planner")
workflow.add_edge("planner", "web_research")
workflow.add_edge("web_research", "rag_research")
workflow.add_edge("rag_research", "research")
workflow.add_edge("research", "verification")


workflow.add_conditional_edges(
    "verification",
    verification_router,
    {
        "retry": "research",
        "end": END,
    },
)


research_graph = workflow.compile()