from fastapi import APIRouter, BackgroundTasks, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.pagination import PaginatedProductResponse
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate
from app.services import product_service

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    product: ProductCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    return product_service.create_product(
        db=db,
        product=product,
        background_tasks=background_tasks,
    )


@router.get("", response_model=PaginatedProductResponse)
def get_products(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return product_service.get_products(
        db=db,
        page=page,
        page_size=page_size,
    )


@router.get("/restock", response_model=list[ProductResponse])
def get_products_to_restock(db: Session = Depends(get_db)):
    return product_service.get_products_to_restock(db=db)


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    return product_service.get_product(db=db, product_id=product_id)


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product: ProductUpdate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    return product_service.update_product(
        db=db,
        product_id=product_id,
        product=product,
        background_tasks=background_tasks,
    )


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product_service.delete_product(db=db, product_id=product_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
