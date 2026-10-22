from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
    status,
)
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.file_metadata import FileMetadataResponse
from app.services import file_metadata_service

router = APIRouter(prefix="/files", tags=["Files"])


@router.post(
    "/upload",
    response_model=FileMetadataResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    return await file_metadata_service.upload_file(db, file)


@router.get("", response_model=list[FileMetadataResponse])
def read_files(db: Session = Depends(get_db)):
    return file_metadata_service.list_files(db)


@router.get("/{file_id}", response_model=FileMetadataResponse)
def read_file(
    file_id: int,
    db: Session = Depends(get_db),
):
    return file_metadata_service.get_file_by_id(db, file_id)


@router.get("/{file_id}/download")
def download_file(
    file_id: int,
    db: Session = Depends(get_db),
):
    file_path = file_metadata_service.get_download_path(db, file_id)
    file_data = file_metadata_service.get_file_by_id(db, file_id)

    return FileResponse(
        path=file_path,
        media_type=file_data.content_type,
        filename=file_data.original_filename,
    )


@router.delete("/{file_id}", status_code=status.HTTP_200_OK)
def delete_file(
    file_id: int,
    db: Session = Depends(get_db),
):
    return file_metadata_service.remove_file(db, file_id)