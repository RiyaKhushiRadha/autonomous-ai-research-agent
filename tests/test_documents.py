from io import BytesIO

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_document_upload():
    file_content = b"Sample research document content."

    response = client.post(
        "/documents/upload",
        files={
            "file": (
                "sample.txt",
                BytesIO(file_content),
                "text/plain",
            )
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["filename"] == "sample.txt"
    assert data["message"] == "Document uploaded and indexed successfully."
    assert data["document_id"]


def test_docx_document_upload():
    from docx import Document

    document = Document()
    document.add_paragraph("Sample DOCX research document content.")

    buffer = BytesIO()
    document.save(buffer)
    buffer.seek(0)

    response = client.post(
        "/documents/upload",
        files={
            "file": (
                "sample.docx",
                buffer,
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["filename"] == "sample.docx"
    assert data["message"] == "Document uploaded and indexed successfully."
    assert data["document_id"]


def test_list_documents():
    file_content = b"Document for list test."

    upload_response = client.post(
        "/documents/upload",
        files={
            "file": (
                "list_test.txt",
                BytesIO(file_content),
                "text/plain",
            )
        },
    )

    assert upload_response.status_code == 200

    uploaded = upload_response.json()

    response = client.get("/documents")

    assert response.status_code == 200

    data = response.json()

    assert "documents" in data
    assert any(
        document["document_id"] == uploaded["document_id"]
        for document in data["documents"]
    )


def test_delete_document():
    file_content = b"Document for delete test."

    upload_response = client.post(
        "/documents/upload",
        files={
            "file": (
                "delete_test.txt",
                BytesIO(file_content),
                "text/plain",
            )
        },
    )

    assert upload_response.status_code == 200

    uploaded = upload_response.json()
    document_id = uploaded["document_id"]

    delete_response = client.delete(
        f"/documents/{document_id}"
    )

    assert delete_response.status_code == 200

    data = delete_response.json()

    assert data["document_id"] == document_id
    assert data["filename"] == "delete_test.txt"
    assert data["message"] == "Document deleted successfully."

    list_response = client.get("/documents")

    assert list_response.status_code == 200

    documents = list_response.json()["documents"]

    assert all(
        document["document_id"] != document_id
        for document in documents
    )


def test_upload_unsupported_file_type():
    file_content = b"Unsupported file content."

    response = client.post(
        "/documents/upload",
        files={
            "file": (
                "sample.csv",
                BytesIO(file_content),
                "text/csv",
            )
        },
    )

    assert response.status_code == 400

    data = response.json()

    assert (
        data["detail"]
        == "Only PDF, DOCX and TXT files are supported."
    )


def test_upload_empty_file():
    response = client.post(
        "/documents/upload",
        files={
            "file": (
                "empty.txt",
                BytesIO(b""),
                "text/plain",
            )
        },
    )

    assert response.status_code == 400

    data = response.json()

    assert data["detail"] == "Uploaded file is empty."


def test_upload_file_too_large():
    large_content = b"x" * (10 * 1024 * 1024 + 1)

    response = client.post(
        "/documents/upload",
        files={
            "file": (
                "large.txt",
                BytesIO(large_content),
                "text/plain",
            )
        },
    )

    assert response.status_code == 400

    data = response.json()

    assert (
        data["detail"]
        == "File size exceeds the maximum allowed limit of 10 MB."
    )

