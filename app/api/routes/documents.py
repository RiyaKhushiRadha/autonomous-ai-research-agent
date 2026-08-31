from fastapi import APIRouter, UploadFile, File, HTTPException

from app.models.documents import (
    DocumentUploadResponse,
    DocumentListResponse,
    DocumentDeleteResponse,
)

from app.services.document_service import document_service


router = APIRouter(tags=["Documents"])


@router.post(
    "/documents/upload", response_model=DocumentUploadResponse,
    summary="Upload a document for RAG",
    description="Uploads a PDF, DOCX, or TXT file (max 10 MB), chunks it, embeds it, and indexes it for retrieval.",
)
async def upload_document(file: UploadFile = File(...)):
    try:
        return await document_service.upload_document(file)

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc


@router.get(
    "/documents", response_model=DocumentListResponse,
    summary="List uploaded documents",
    description="Returns all documents currently indexed and available for retrieval.",
)
async def list_documents():
    return {
        "documents": document_service.list_documents()
    }


@router.delete(
    "/documents/{document_id}", response_model=DocumentDeleteResponse,
    summary="Delete a document",
    description="Removes a document and its chunks from the index.",
)
async def delete_document(document_id: str):
    try:
        return document_service.delete_document(document_id)

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc