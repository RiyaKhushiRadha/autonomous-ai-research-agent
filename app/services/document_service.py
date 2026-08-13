from pathlib import Path
import tempfile

from app.rag.loader import load_pdf
from app.rag.splitter import split_text
from app.rag.embeddings import create_embeddings
from app.rag.vector_store import vector_store


class DocumentService:

    async def upload_document(self, file) -> dict:
        suffix = Path(file.filename).suffix.lower()

        content = await file.read()

        if suffix == ".pdf":
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                temp_file.write(content)
                temp_file_path = temp_file.name

            text = load_pdf(temp_file_path)

        elif suffix == ".txt":
            text = content.decode("utf-8")

        else:
            raise ValueError("Only PDF and TXT files are supported.")

        chunks = split_text(text)
        embeddings = create_embeddings(chunks)

        vector_store.add_documents(chunks, embeddings)

        return {
            "filename": file.filename,
            "message": "Document uploaded and indexed successfully.",
        }


document_service = DocumentService()