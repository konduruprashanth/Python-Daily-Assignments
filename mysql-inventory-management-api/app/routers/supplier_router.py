from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.supplier import (
    SupplierCreate,
    SupplierResponse,
    SupplierUpdate,
)
from app.services import supplier_service

router = APIRouter(prefix="/suppliers", tags=["Suppliers"])


@router.post(
    "",
    response_model=SupplierResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_supplier(
    supplier: SupplierCreate,
    db: Session = Depends(get_db),
):
    return supplier_service.create_supplier(db, supplier)


@router.get("", response_model=list[SupplierResponse])
def read_suppliers(
    active_only: bool = False,
    db: Session = Depends(get_db),
):
    return supplier_service.get_suppliers(db, active_only=active_only)


@router.get("/active", response_model=list[SupplierResponse])
def read_active_suppliers(db: Session = Depends(get_db)):
    return supplier_service.get_active_suppliers(db)


@router.get("/{supplier_id}", response_model=SupplierResponse)
def read_supplier(
    supplier_id: int,
    db: Session = Depends(get_db),
):
    return supplier_service.get_supplier(db, supplier_id)


@router.put("/{supplier_id}", response_model=SupplierResponse)
def update_supplier(
    supplier_id: int,
    supplier: SupplierUpdate,
    db: Session = Depends(get_db),
):
    return supplier_service.update_supplier(db, supplier_id, supplier)


@router.delete(
    "/{supplier_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_supplier(
    supplier_id: int,
    db: Session = Depends(get_db),
):
    supplier_service.delete_supplier(db, supplier_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
