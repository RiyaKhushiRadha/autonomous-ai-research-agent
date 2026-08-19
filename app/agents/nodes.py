from app.agents.state import ResearchState

from app.tools.web_search import search_web

from app.tools.retrieval import retrieve_documents_tool

from app.services.llm_service import generate_text

from app.agents.prompts import (
    planner_prompt,
    research_prompt,
    verification_prompt,
)

async def research_node(state: ResearchState) -> ResearchState:
    query = state["query"]
    plan = state.get("plan", "")
    web_results = state.get("web_results", [])
    rag_results = state.get("rag_results", [])

    prompt = research_prompt.format(
        query=query,
        plan=plan,
        web_results=web_results,
        rag_results=rag_results,
    )

    final_answer = await generate_text(prompt)

    return {
        **state,
        "final_answer": final_answer,
    }

async def planner_node(state: ResearchState) -> ResearchState:
    query = state["query"]

    prompt = planner_prompt.format(
        query=query,
    )

    plan = await generate_text(prompt)

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

    results = retrieve_documents_tool.invoke(
        {"query": query}
    )

    return {
        **state,
        "rag_results": results,
    }

async def verification_node(state: ResearchState) -> ResearchState:
    query = state["query"]
    final_answer = state.get("final_answer", "")
    web_results = state.get("web_results", [])
    rag_results = state.get("rag_results", [])
    retry_count = state.get("retry_count", 0)

    prompt = verification_prompt.format(
        query=query,
        final_answer=final_answer,
        web_results=web_results,
        rag_results=rag_results,
    )

    result = await generate_text(prompt)

    import json

    try:
        verification = json.loads(result)
    except json.JSONDecodeError:
        verification = {
            "verified": False,
            "reason": "Verification response could not be parsed.",
        }

    if verification.get("verified") is False:
        retry_count += 1

    return {
        **state,
        "verification": verification,
        "retry_count": retry_count,
    }
