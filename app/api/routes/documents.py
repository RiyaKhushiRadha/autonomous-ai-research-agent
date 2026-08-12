from fastapi import APIRouter, UploadFile, File

from app.models.documents import DocumentUploadResponse
from app.services.document_service import document_service


router = APIRouter()


@router.post("/documents/upload", response_model=DocumentUploadResponse)
async def upload_document(file: UploadFile = File(...)):
    return await document_service.upload_document(file.filename)