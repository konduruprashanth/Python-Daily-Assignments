from sqlalchemy.orm import Session

from app.models.file_metadata import FileMetadata


def create_file_metadata(db: Session, file_data: dict):
    db_file = FileMetadata(**file_data)
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file


def get_files(db: Session):
    return (
        db.query(FileMetadata)
        .order_by(FileMetadata.uploaded_at.desc())
        .all()
    )


def get_file(db: Session, file_id: int):
    return (
        db.query(FileMetadata)
        .filter(FileMetadata.id == file_id)
        .first()
    )


def delete_file_metadata(db: Session, db_file: FileMetadata):
    db.delete(db_file)
    db.commit()
    return True