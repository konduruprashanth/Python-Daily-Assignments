from datetime import datetime

from pydantic import Field

from app.schemas.category import ORMBase


class FileMetadataResponse(ORMBase):
    id: int
    original_filename: str
    stored_filename: str
    file_path: str
    content_type: str
    file_size: int = Field(ge=0)
    uploaded_at: datetime
