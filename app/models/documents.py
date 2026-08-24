from pydantic import BaseModel


class DocumentUploadResponse(BaseModel):
    document_id: str
    filename: str
    message: str


class DocumentResponse(BaseModel):
    document_id: str
    filename: str
    status: str


class DocumentListResponse(BaseModel):
    documents: list[DocumentResponse]


class DocumentDeleteResponse(BaseModel):
    document_id: str
    filename: str
    message: str