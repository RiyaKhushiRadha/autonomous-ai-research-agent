from app.rag.retriever import retrieve_documents
from app.rag.vector_store import vector_store


if not vector_store.documents:
    print("No document is currently indexed.")
    print("Upload a PDF first and run the test in the same process.")
else:
    query = input("Ask a question about the uploaded document: ")

    results = retrieve_documents(
        query=query,
        top_k=3,
    )

    print("\nRetrieved Document Chunks:\n")

    for index, result in enumerate(results, start=1):
        print(f"\n--- Result {index} ---")
        print(result)