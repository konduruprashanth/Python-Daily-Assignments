from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.repositories import category_repository
from app.schemas.category import CategoryCreate, CategoryUpdate


def create_category(db: Session, category: CategoryCreate):
    try:
        return category_repository.create_category(db, category)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "The operation violates a database constraint. "
                "Check duplicate values and related records."
            ),
        )


def get_categories(db: Session):
    return category_repository.get_categories(db)


def get_category(db: Session, category_id: int):
    category = category_repository.get_category(db, category_id)

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )

    return category


def update_category(
    db: Session,
    category_id: int,
    category: CategoryUpdate,
):
    try:
        updated_category = category_repository.update_category(
            db, category_id, category
        )
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "The operation violates a database constraint. "
                "Check duplicate values and related records."
            ),
        )

    if updated_category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )

    return updated_category


def delete_category(db: Session, category_id: int):
    try:
        deleted = category_repository.delete_category(db, category_id)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "The operation violates a database constraint. "
                "Check duplicate values and related records."
            ),
        )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )
