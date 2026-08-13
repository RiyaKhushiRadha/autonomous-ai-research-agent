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