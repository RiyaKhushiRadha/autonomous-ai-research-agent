from fastapi import APIRouter, UploadFile, File, HTTPException

from app.models.documents import (
    DocumentUploadResponse,
    DocumentListResponse,
    DocumentDeleteResponse,
)

from app.services.document_service import document_service


router = APIRouter()


@router.post(
    "/documents/upload",
    response_model=DocumentUploadResponse,
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
    "/documents",
    response_model=DocumentListResponse,
)
async def list_documents():
    return {
        "documents": document_service.list_documents()
    }


@router.delete(
    "/documents/{document_id}",
    response_model=DocumentDeleteResponse,
)
async def delete_document(document_id: str):
    try:
        return document_service.delete_document(document_id)

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc