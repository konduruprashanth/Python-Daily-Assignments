from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.repositories import supplier_repository
from app.schemas.supplier import SupplierCreate, SupplierUpdate


def create_supplier(db: Session, supplier: SupplierCreate):
    try:
        return supplier_repository.create_supplier(db, supplier)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "The operation violates a database constraint. "
                "Check duplicate values and related records."
            ),
        )


def get_suppliers(db: Session, active_only: bool = False):
    return supplier_repository.get_suppliers(db, active_only=active_only)


def get_active_suppliers(db: Session):
    return supplier_repository.get_active_suppliers(db)


def get_supplier(db: Session, supplier_id: int):
    supplier = supplier_repository.get_supplier(db, supplier_id)

    if supplier is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Supplier not found",
        )

    return supplier


def update_supplier(
    db: Session,
    supplier_id: int,
    supplier: SupplierUpdate,
):
    try:
        updated_supplier = supplier_repository.update_supplier(
            db, supplier_id, supplier
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

    if updated_supplier is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Supplier not found",
        )

    return updated_supplier


def delete_supplier(db: Session, supplier_id: int):
    try:
        deleted = supplier_repository.delete_supplier(db, supplier_id)
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
            detail="Supplier not found",
        )