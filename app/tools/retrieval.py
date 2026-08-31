from langchain_core.tools import tool

from app.rag.retriever import DocumentRetriever


@tool
def retrieve_documents_tool(
    query: str,
    document_ids: list[str] | None = None,
) -> list[str]:
    """
    Retrieve relevant information from uploaded documents for a research query.
    """
    retriever = DocumentRetriever(top_k=3, document_ids=document_ids)

    documents = retriever.invoke(query)

    return [
        document.page_content
        for document in documents
    ]
