from app.agents.state import ResearchState

from app.tools.web_search import search_web

from app.rag.retriever import retrieve_documents

def research_node(state: ResearchState) -> ResearchState:
    query = state["query"]

    web_results = state.get("web_results", [])
    rag_results = state.get("rag_results", [])

    answer_parts = [
        f"Research findings for: {query}",
        "",
        "Web Research:",
    ]

    for result in web_results[:3]:
        answer_parts.append(
            f"- {result.get('title', '')}: {result.get('content', '')}"
        )

    answer_parts.append("")
    answer_parts.append("Uploaded Document Research:")

    for result in rag_results[:3]:
        answer_parts.append(f"- {result}")

    final_answer = "\n".join(answer_parts)

    return {
        **state,
        "final_answer": final_answer,
    }

def planner_node(state: ResearchState) -> ResearchState:
    query = state["query"]

    plan = (
        f"1. Understand the research question: {query}\n"
        "2. Search for relevant information from web sources.\n"
        "3. Check relevant information from uploaded documents.\n"
        "4. Combine the research findings.\n"
        "5. Verify the important information before producing the final answer."
    )

    return {
        **state,
        "plan": plan,
    }

def web_research_node(state: ResearchState) -> ResearchState:
    query = state["query"]

    results = search_web(query)

    web_results = []

    for result in results.get("results", []):
        web_results.append(
            {
                "title": result.get("title", ""),
                "url": result.get("url", ""),
                "content": result.get("content", ""),
                "score": result.get("score", 0),
            }
        )

    return {
        **state,
        "web_results": web_results,
    }

def rag_research_node(state: ResearchState) -> ResearchState:
    query = state["query"]

    results = retrieve_documents(
        query=query,
        top_k=3,
    )

    return {
        **state,
        "rag_results": results,
    }

def verification_node(state: ResearchState) -> ResearchState:
    web_results = state.get("web_results", [])
    rag_results = state.get("rag_results", [])

    verification = {
        "web_sources_found": len(web_results),
        "document_sources_found": len(rag_results),
        "verified": bool(web_results or rag_results),
    }

    return {
        **state,
        "verification": verification,
    }

