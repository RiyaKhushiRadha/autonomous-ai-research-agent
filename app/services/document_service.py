from pathlib import Path
import tempfile
import uuid

from app.rag.loader import load_pdf, load_docx
from app.rag.splitter import split_text
from app.rag.embeddings import create_embeddings
from app.rag.vector_store import vector_store


MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

SUPPORTED_EXTENSIONS = {".pdf", ".txt", ".docx"}


class DocumentService:

    def __init__(self):
        self.documents = {}

    async def upload_document(self, file) -> dict:
        filename = file.filename or ""
        suffix = Path(filename).suffix.lower()

        if suffix not in SUPPORTED_EXTENSIONS:
            raise ValueError(
                "Only PDF, DOCX and TXT files are supported."
            )

        content = await file.read()

        if not content:
            raise ValueError("Uploaded file is empty.")

        if len(content) > MAX_FILE_SIZE:
            raise ValueError(
                "File size exceeds the maximum allowed limit of 10 MB."
            )

        document_id = str(uuid.uuid4())

        if suffix == ".pdf":
            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".pdf",
            ) as temp_file:
                temp_file.write(content)
                temp_file_path = temp_file.name

            text = load_pdf(temp_file_path)

        elif suffix == ".docx":
            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".docx",
            ) as temp_file:
                temp_file.write(content)
                temp_file_path = temp_file.name

            text = load_docx(temp_file_path)

        else:
            text = content.decode("utf-8")

        if not text.strip():
            raise ValueError("Uploaded document contains no readable text.")

        chunks = split_text(text)

        if not chunks:
            raise ValueError("Document could not be split into readable chunks.")

        embeddings = create_embeddings(chunks)

        vector_store.add_documents(
            chunks,
            embeddings,
            document_id,
        )

        self.documents[document_id] = {
            "document_id": document_id,
            "filename": filename,
            "status": "indexed",
        }

        return {
            "document_id": document_id,
            "filename": filename,
            "message": "Document uploaded and indexed successfully.",
        }

    def list_documents(self) -> list[dict]:
        return list(self.documents.values())

    def delete_document(self, document_id: str) -> dict:
        if document_id not in self.documents:
            raise ValueError("Document not found.")

        deleted = vector_store.delete_document(document_id)

        if not deleted:
            raise ValueError("Document data not found in vector store.")

        document = self.documents.pop(document_id)

        return {
            "document_id": document_id,
            "filename": document["filename"],
            "message": "Document deleted successfully.",
        }


document_service = DocumentService()