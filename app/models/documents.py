from pydantic import BaseModel


class DocumentUploadResponse(BaseModel):
    filename: str
    message: str


class DocumentResponse(BaseModel):
    filename: str
    status: str


class DocumentListResponse(BaseModel):
    documents: list[DocumentResponse]