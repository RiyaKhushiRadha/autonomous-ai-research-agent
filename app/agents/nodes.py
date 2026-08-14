from app.agents.state import ResearchState

from app.tools.web_search import search_web

from app.rag.retriever import retrieve_documents

from app.services.llm_service import generate_text

async def research_node(state: ResearchState) -> ResearchState:
    query = state["query"]
    plan = state.get("plan", "")
    web_results = state.get("web_results", [])
    rag_results = state.get("rag_results", [])

    prompt = f"""
You are an AI research assistant.

Research Question:
{query}

Research Plan:
{plan}

Web Research:
{web_results}

Uploaded Document Research:
{rag_results}

Using the available research information, generate a clear and accurate answer.

Rules:
- Use the provided research information.
- Do not invent facts.
- If the available information is insufficient, clearly say so.
- Keep the answer concise and useful.
"""

    final_answer = await generate_text(prompt)

    return {
        **state,
        "final_answer": final_answer,
    }

async def planner_node(state: ResearchState) -> ResearchState:
    query = state["query"]

    prompt = f"""
You are a research planning agent.

Create a clear research plan for this question:

{query}

The plan should include:
1. What needs to be understood
2. What information should be searched on the web
3. What information should be checked from uploaded documents
4. How the findings should be combined
5. What should be verified before the final answer

Return only the research plan.
"""

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

    results = retrieve_documents(
        query=query,
        top_k=3,
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

    prompt = f"""
You are a research verification agent.

Research Question:
{query}

Generated Answer:
{final_answer}

Available Web Evidence:
{web_results}

Available Document Evidence:
{rag_results}

Check whether the generated answer is properly supported by the available evidence.

Return ONLY valid JSON in this format:

{{
    "verified": true,
    "reason": "short explanation"
}}

Set "verified" to false if the answer contains unsupported or unreliable information.
"""

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
