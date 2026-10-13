from sqlalchemy.orm import Session
from sqlalchemy import func

from app import models, schemas


# ---------------- CATEGORY CRUD ----------------

def create_category(db: Session, category: schemas.CategoryCreate):
    existing_category = (
        db.query(models.Category)
        .filter(models.Category.name == category.name)
        .first()
    )

    if existing_category:
        return None

    db_category = models.Category(**category.model_dump())

    try:
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return db_category
    except Exception:
        db.rollback()
        raise


def get_categories(db: Session):
    return db.query(models.Category).all()


def get_category(db: Session, category_id: int):
    return (
        db.query(models.Category)
        .filter(models.Category.id == category_id)
        .first()
    )


def update_category(
    db: Session,
    category_id: int,
    category: schemas.CategoryUpdate,
):
    db_category = get_category(db, category_id)

    if not db_category:
        return None

    update_data = category.model_dump(exclude_unset=True)

    if "name" in update_data:
        existing_category = (
            db.query(models.Category)
            .filter(
                models.Category.name == update_data["name"],
                models.Category.id != category_id,
            )
            .first()
        )

        if existing_category:
            return "duplicate"

    for key, value in update_data.items():
        setattr(db_category, key, value)

    try:
        db.commit()
        db.refresh(db_category)
        return db_category
    except Exception:
        db.rollback()
        raise


def delete_category(db: Session, category_id: int):
    db_category = get_category(db, category_id)

    if not db_category:
        return None

    if db_category.products:
        return "has_products"

    try:
        db.delete(db_category)
        db.commit()
        return db_category
    except Exception:
        db.rollback()
        raise


# ---------------- PRODUCT CRUD ----------------

def create_product(db: Session, product: schemas.ProductCreate):
    category = get_category(db, product.category_id)

    if not category:
        return None

    db_product = models.Product(**product.model_dump())

    try:
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product
    except Exception:
        db.rollback()
        raise


def get_products(
    db: Session,
    category_id: int | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    search: str | None = None,
):
    query = db.query(models.Product)

    if category_id is not None:
        query = query.filter(
            models.Product.category_id == category_id
        )

    if min_price is not None:
        query = query.filter(
            models.Product.price >= min_price
        )

    if max_price is not None:
        query = query.filter(
            models.Product.price <= max_price
        )

    if search:
        query = query.filter(
            models.Product.name.ilike(f"%{search}%")
        )

    return query.all()


def get_product(db: Session, product_id: int):
    return (
        db.query(models.Product)
        .filter(models.Product.id == product_id)
        .first()
    )


def update_product(
    db: Session,
    product_id: int,
    product: schemas.ProductUpdate,
):
    db_product = get_product(db, product_id)

    if not db_product:
        return None

    update_data = product.model_dump(exclude_unset=True)

    if (
        "category_id" in update_data
        and update_data["category_id"] is not None
    ):
        category = get_category(db, update_data["category_id"])

        if not category:
            return "invalid_category"

    for key, value in update_data.items():
        setattr(db_product, key, value)

    try:
        db.commit()
        db.refresh(db_product)
        return db_product
    except Exception:
        db.rollback()
        raise


def delete_product(db: Session, product_id: int):
    db_product = get_product(db, product_id)

    if not db_product:
        return None

    try:
        db.delete(db_product)
        db.commit()
        return db_product
    except Exception:
        db.rollback()
        raise


def get_category_products(db: Session, category_id: int):
    return (
        db.query(models.Product)
        .filter(models.Product.category_id == category_id)
        .all()
    )


def get_inventory_value(db: Session):
    result = db.query(
        func.coalesce(
            func.sum(models.Product.price * models.Product.quantity),
            0,
        )
    ).scalar()

    return result