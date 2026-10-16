from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.repositories import product_repository
from app.schemas.product import ProductCreate, ProductUpdate


def create_product(db: Session, product: ProductCreate):
    try:
        return product_repository.create_product(db, product)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "The operation violates a database constraint. "
                "Check duplicate values and related records."
            ),
        )


def get_products(db: Session):
    return product_repository.get_products(db)


def get_products_to_restock(db: Session):
    return product_repository.get_products_to_restock(db)


def get_product(db: Session, product_id: int):
    product = product_repository.get_product(db, product_id)

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    return product


def get_product_by_sku(db: Session, sku: str):
    return product_repository.get_product_by_sku(db, sku)


def update_product(
    db: Session,
    product_id: int,
    product: ProductUpdate,
):
    try:
        updated_product = product_repository.update_product(
            db, product_id, product
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

    if updated_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    return updated_product


def delete_product(db: Session, product_id: int):
    try:
        deleted = product_repository.delete_product(db, product_id)
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
            detail="Product not found",
        )