class DocumentService:

    async def upload_document(self, filename: str) -> dict:
        return {
            "filename": filename,
            "message": "Document upload endpoint is ready.",
        }


document_service = DocumentService()