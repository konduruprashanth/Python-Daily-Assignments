from sqlalchemy.orm import Session

from app.models.supplier import Supplier
from app.schemas.supplier import SupplierCreate, SupplierUpdate


def create_supplier(db: Session, supplier: SupplierCreate):
    db_supplier = Supplier(**supplier.model_dump())
    db.add(db_supplier)
    db.commit()
    db.refresh(db_supplier)
    return db_supplier


def get_suppliers(db: Session, active_only: bool = False):
    query = db.query(Supplier)

    if active_only:
        query = query.filter(Supplier.is_active.is_(True))

    return query.all()


def get_active_suppliers(db: Session):
    return get_suppliers(db, active_only=True)


def get_supplier(db: Session, supplier_id: int):
    return db.query(Supplier).filter(Supplier.supplier_id == supplier_id).first()


def update_supplier(
    db: Session,
    supplier_id: int,
    supplier: SupplierUpdate,
):
    db_supplier = get_supplier(db, supplier_id)

    if db_supplier is None:
        return None

    update_data = supplier.model_dump(exclude_unset=True, mode="json")

    for key, value in update_data.items():
        setattr(db_supplier, key, value)

    db.commit()
    db.refresh(db_supplier)
    return db_supplier


def delete_supplier(db: Session, supplier_id: int):
    db_supplier = get_supplier(db, supplier_id)

    if db_supplier is None:
        return False

    db.delete(db_supplier)
    db.commit()
    return True
