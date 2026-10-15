from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import models, schemas


# Category CRUD operations
def create_category(db: Session, category: schemas.CategoryCreate):
    db_category = models.Category(**category.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def get_categories(db: Session):
    return db.query(models.Category).all()


def get_category(db: Session, category_id: int):
    return (
        db.query(models.Category)
        .filter(models.Category.category_id == category_id)
        .first()
    )


def update_category(
    db: Session,
    category_id: int,
    category: schemas.CategoryUpdate,
):
    db_category = get_category(db, category_id)

    if db_category is None:
        return None

    update_data = category.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_category, key, value)

    db.commit()
    db.refresh(db_category)
    return db_category


def delete_category(db: Session, category_id: int):
    db_category = get_category(db, category_id)

    if db_category is None:
        return False

    db.delete(db_category)
    db.commit()
    return True


# Supplier CRUD operations
def create_supplier(db: Session, supplier: schemas.SupplierCreate):
    db_supplier = models.Supplier(**supplier.model_dump())
    db.add(db_supplier)
    db.commit()
    db.refresh(db_supplier)
    return db_supplier


def get_suppliers(db: Session, active_only: bool = False):
    query = db.query(models.Supplier)

    if active_only:
        query = query.filter(models.Supplier.is_active.is_(True))

    return query.all()


def get_active_suppliers(db: Session):
    return get_suppliers(db, active_only=True)


def get_supplier(db: Session, supplier_id: int):
    return (
        db.query(models.Supplier)
        .filter(models.Supplier.supplier_id == supplier_id)
        .first()
    )


def update_supplier(
    db: Session,
    supplier_id: int,
    supplier: schemas.SupplierUpdate,
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


# Product CRUD operations
def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(**product.model_dump())
    db.add(db_product)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise

    db.refresh(db_product)
    return db_product


def get_products(db: Session):
    return db.query(models.Product).all()


def get_products_to_restock(db: Session):
    return (
        db.query(models.Product)
        .filter(models.Product.quantity <= models.Product.reorder_level)
        .all()
    )


def get_product(db: Session, product_id: int):
    return (
        db.query(models.Product).filter(models.Product.product_id == product_id).first()
    )


def get_product_by_sku(db: Session, sku: str):
    return db.query(models.Product).filter(models.Product.sku == sku).first()


def update_product(
    db: Session,
    product_id: int,
    product: schemas.ProductUpdate,
):
    db_product = get_product(db, product_id)

    if db_product is None:
        return None

    update_data = product.model_dump(exclude_unset=True, mode="json")

    for key, value in update_data.items():
        setattr(db_product, key, value)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise

    db.refresh(db_product)
    return db_product


def delete_product(db: Session, product_id: int):
    db_product = get_product(db, product_id)

    if db_product is None:
        return False

    db.delete(db_product)
    db.commit()
    return True
