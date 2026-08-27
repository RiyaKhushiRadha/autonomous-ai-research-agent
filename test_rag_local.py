from app.agents.nodes import rag_research_node
from app.rag.embeddings import create_embeddings
from app.rag.vector_store import vector_store


def test_rag_research_node_local():
    text = """
            Retrieval Augmented Generation (RAG) allows an AI system to retrieve
            relevant information from external documents before generating an answer.

            RAG improves factual accuracy by grounding responses in retrieved information.

            LangGraph is used to build stateful, multi-step AI agent workflows.

            FastAPI is a Python framework for building APIs.
        """

    chunks = [
        text.split("\n\n")[0],
        text.split("\n\n")[1],
        text.split("\n\n")[2],
    ]

    embeddings = create_embeddings(chunks)

    vector_store.add_documents(
        documents=chunks,
        embeddings=embeddings,
        document_id="local-test-doc",
    )

    state = {
        "query": "How does RAG improve factual accuracy?",
        "rag_results": [],
    }

    result = rag_research_node(state)

    assert isinstance(result["rag_results"], list)
    assert len(result["rag_results"]) > 0