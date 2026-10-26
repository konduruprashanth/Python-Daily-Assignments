from unittest.mock import patch

VALID_PDF = b"%PDF-1.4\nTest PDF content\n%%EOF"


def upload_test_pdf(client):
    return client.post(
        "/files/upload",
        files={
            "file": (
                "test-document.pdf",
                VALID_PDF,
                "application/pdf",
            )
        },
    )


def test_upload_file(client, tmp_path):
    with patch("app.services.file_metadata_service.UPLOAD_DIR", tmp_path):
        response = upload_test_pdf(client)
        assert response.status_code == 201, response.text

        data = response.json()
        assert data["id"] > 0
        assert data["original_filename"] == "test-document.pdf"
        assert data["content_type"] == "application/pdf"
        assert data["file_size"] == len(VALID_PDF)

        stored_file = tmp_path / data["stored_filename"]
        assert stored_file.exists()
        assert stored_file.read_bytes() == VALID_PDF


def test_list_files(client, tmp_path):
    with patch("app.services.file_metadata_service.UPLOAD_DIR", tmp_path):
        upload_response = upload_test_pdf(client)
        assert upload_response.status_code == 201, upload_response.text

        response = client.get("/files")
        assert response.status_code == 200, response.text
        assert len(response.json()) == 1
        assert response.json()[0]["original_filename"] == "test-document.pdf"


def test_get_file_metadata(client, tmp_path):
    with patch("app.services.file_metadata_service.UPLOAD_DIR", tmp_path):
        upload_response = upload_test_pdf(client)
        assert upload_response.status_code == 201, upload_response.text

        file_id = upload_response.json()["id"]
        response = client.get(f"/files/{file_id}")

        assert response.status_code == 200, response.text
        assert response.json()["id"] == file_id
        assert response.json()["original_filename"] == "test-document.pdf"


def test_download_file(client, tmp_path):
    with patch("app.services.file_metadata_service.UPLOAD_DIR", tmp_path):
        upload_response = upload_test_pdf(client)
        assert upload_response.status_code == 201, upload_response.text

        file_id = upload_response.json()["id"]
        response = client.get(f"/files/{file_id}/download")

        assert response.status_code == 200, (
            f"Download failed: status={response.status_code}, response={response.text}"
        )
        assert response.content == VALID_PDF
        assert "application/pdf" in response.headers["content-type"]


def test_delete_file(client, tmp_path):
    with patch("app.services.file_metadata_service.UPLOAD_DIR", tmp_path):
        upload_response = upload_test_pdf(client)
        assert upload_response.status_code == 201, upload_response.text

        data = upload_response.json()
        file_id = data["id"]
        stored_file = tmp_path / data["stored_filename"]
        assert stored_file.exists()

        response = client.delete(f"/files/{file_id}")

        assert response.status_code == 200, (
            f"Delete failed: status={response.status_code}, response={response.text}"
        )
        assert response.json()["message"] == "File deleted successfully."
        assert not stored_file.exists()

        get_response = client.get(f"/files/{file_id}")
        assert get_response.status_code == 404


def test_upload_rejects_unsupported_file_type(client):
    response = client.post(
        "/files/upload",
        files={"file": ("test.txt", b"Test text content", "text/plain")},
    )
    assert response.status_code == 400


def test_upload_rejects_empty_file(client):
    response = client.post(
        "/files/upload",
        files={"file": ("empty.pdf", b"", "application/pdf")},
    )
    assert response.status_code == 400


def test_upload_rejects_invalid_pdf_content(client):
    response = client.post(
        "/files/upload",
        files={
            "file": (
                "invalid.pdf",
                b"This is not a valid PDF signature",
                "application/pdf",
            )
        },
    )
    assert response.status_code == 400


def test_upload_rejects_mismatched_content_type(client):
    response = client.post(
        "/files/upload",
        files={"file": ("test.pdf", VALID_PDF, "image/jpeg")},
    )
    assert response.status_code == 400


def test_missing_file_returns_not_found(client):
    response = client.get("/files/99999")
    assert response.status_code == 404


def test_missing_file_download_returns_not_found(client):
    response = client.get("/files/99999/download")
    assert response.status_code == 404


def test_delete_missing_file_returns_not_found(client):
    response = client.delete("/files/99999")
    assert response.status_code == 404
