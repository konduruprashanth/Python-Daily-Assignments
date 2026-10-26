from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


def create_product(db: Session, product: ProductCreate):
    db_product = Product(**product.model_dump())
    db.add(db_product)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise

    db.refresh(db_product)
    return db_product


def get_products(
    db: Session,
    page: int = 1,
    page_size: int = 10,
):
    query = db.query(Product)

    total = query.count()

    products = (
        query.order_by(Product.product_id)
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    return {
        "items": products,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size,
    }


def get_products_to_restock(db: Session):
    return (
        db.query(Product)
        .filter(Product.quantity <= Product.reorder_level)
        .all()
    )


def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.product_id == product_id).first()


def get_product_by_sku(db: Session, sku: str):
    return db.query(Product).filter(Product.sku == sku).first()


def update_product(
    db: Session,
    product_id: int,
    product: ProductUpdate,
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