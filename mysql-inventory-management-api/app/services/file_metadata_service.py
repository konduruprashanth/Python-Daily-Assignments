import uuid
from pathlib import Path

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.repositories.file_metadata_repository import (
    create_file_metadata,
    delete_file_metadata,
    get_file,
    get_files,
)

UPLOAD_DIR = Path("uploads").resolve()
MAX_FILE_SIZE = 5 * 1024 * 1024

ALLOWED_TYPES = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".pdf": "application/pdf",
}


def validate_file_signature(extension: str, content: bytes) -> bool:
    if extension in {".jpg", ".jpeg"}:
        return content.startswith(b"\xff\xd8\xff")

    if extension == ".png":
        return content.startswith(b"\x89PNG\r\n\x1a\n")

    if extension == ".pdf":
        return content.startswith(b"%PDF-")

    return False


async def upload_file(db: Session, file: UploadFile):
    original_filename = Path(file.filename or "").name

    if not original_filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A filename is required.",
        )

    extension = Path(original_filename).suffix.lower()

    if extension not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only JPG, JPEG, PNG, and PDF files are allowed.",
        )

    if file.content_type != ALLOWED_TYPES[extension]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File extension and content type do not match.",
        )

    content = await file.read(MAX_FILE_SIZE + 1)

    if not content:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Empty files are not allowed.",
        )

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="File size must not exceed 5 MB.",
        )

    if not validate_file_signature(extension, content):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The file content does not match its file type.",
        )

    stored_filename = f"{uuid.uuid4().hex}{extension}"
    relative_path = Path("uploads") / stored_filename
    destination = UPLOAD_DIR / stored_filename

    try:
        UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(content)

        file_data = {
            "original_filename": original_filename,
            "stored_filename": stored_filename,
            "file_path": str(relative_path).replace("\\", "/"),
            "content_type": ALLOWED_TYPES[extension],
            "file_size": len(content),
        }

        return create_file_metadata(db, file_data)

    except SQLAlchemyError as exc:
        db.rollback()

        if destination.exists():
            destination.unlink()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not save file metadata.",
        ) from exc

    except OSError as exc:
        db.rollback()

        if destination.exists():
            destination.unlink()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not store the uploaded file.",
        ) from exc

    finally:
        await file.close()


def list_files(db: Session):
    return get_files(db)


def get_file_by_id(db: Session, file_id: int):
    db_file = get_file(db, file_id)

    if db_file is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found.",
        )

    return db_file


def get_download_path(db: Session, file_id: int) -> Path:
    db_file = get_file_by_id(db, file_id)

    stored_filename = db_file.stored_filename
    stored_name = Path(stored_filename)

    # Only allow a single filename, not a directory path.
    if (
        not stored_filename
        or stored_name.name != stored_filename
        or stored_filename in {".", ".."}
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file path.",
        )

    # Validate the saved relative path and ensure it refers to
    # the same filename recorded in the metadata.
    recorded_path = Path(db_file.file_path)

    if (
        recorded_path.is_absolute()
        or ".." in recorded_path.parts
        or recorded_path.name != stored_filename
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file path.",
        )

    upload_root = UPLOAD_DIR.resolve()
    full_path = (upload_root / stored_name).resolve()

    # Prevent directory traversal outside the upload directory.
    if full_path.parent != upload_root:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file path.",
        )

    if not full_path.is_file():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Stored file is missing.",
        )

    return full_path


def remove_file(db: Session, file_id: int):
    db_file = get_file_by_id(db, file_id)
    file_path = get_download_path(db, file_id)

    try:
        delete_file_metadata(db, db_file)
    except SQLAlchemyError as exc:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not delete file metadata.",
        ) from exc

    try:
        file_path.unlink()
    except OSError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=("Metadata was deleted, but the stored file could not be removed."),
        ) from exc

    return {"message": "File deleted successfully."}
