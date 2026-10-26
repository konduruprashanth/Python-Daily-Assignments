import logging

from fastapi import BackgroundTasks, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.product import Product
from app.repositories import product_repository
from app.schemas.product import ProductCreate, ProductUpdate
from app.services.email_service import send_low_stock_alert

logger = logging.getLogger(__name__)


def _handle_low_stock_alert(
    db: Session,
    product: Product,
    background_tasks: BackgroundTasks,
) -> None:
    """Schedule one alert per low-stock period."""
    is_low_stock = product.quantity <= product.reorder_level

    if is_low_stock and not product.low_stock_alert_sent:
        product.low_stock_alert_sent = True

        try:
            db.commit()
            db.refresh(product)
        except Exception:
            db.rollback()
            logger.exception("Could not record low-stock alert status.")
            return

        background_tasks.add_task(
            send_low_stock_alert,
            product.product_name,
            product.sku,
            product.quantity,
            product.reorder_level,
        )

    elif not is_low_stock and product.low_stock_alert_sent:
        product.low_stock_alert_sent = False

        try:
            db.commit()
        except Exception:
            db.rollback()
            logger.exception("Could not reset low-stock alert status.")


def create_product(
    db: Session,
    product: ProductCreate,
    background_tasks: BackgroundTasks,
):
    try:
        db_product = product_repository.create_product(db, product)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "The operation violates a database constraint. "
                "Check duplicate values and related records."
            ),
        )

    _handle_low_stock_alert(db, db_product, background_tasks)
    return db_product


def get_products(
    db: Session,
    page: int = 1,
    page_size: int = 10,
):
    return product_repository.get_products(
        db,
        page=page,
        page_size=page_size,
    )


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
    background_tasks: BackgroundTasks,
):
    try:
        updated_product = product_repository.update_product(
            db,
            product_id,
            product,
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

    _handle_low_stock_alert(db, updated_product, background_tasks)
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
