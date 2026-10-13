from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import Base, engine, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Inventory Management API",
    description="Manage products, categories, and suppliers.",
    version="1.0.0",
)


def handle_integrity_error(db: Session):
    db.rollback()
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=(
            "The operation violates a database constraint. "
            "Check duplicate values and related records."
        ),
    )


# Category endpoints
@app.post(
    "/categories",
    response_model=schemas.CategoryResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_category(
    category: schemas.CategoryCreate,
    db: Session = Depends(get_db),
):
    try:
        return crud.create_category(db, category)
    except IntegrityError:
        handle_integrity_error(db)


@app.get("/categories", response_model=list[schemas.CategoryResponse])
def read_categories(db: Session = Depends(get_db)):
    return crud.get_categories(db)


@app.get(
    "/categories/{category_id}",
    response_model=schemas.CategoryResponse,
)
def read_category(
    category_id: int,
    db: Session = Depends(get_db),
):
    category = crud.get_category(db, category_id)

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )

    return category


@app.put(
    "/categories/{category_id}",
    response_model=schemas.CategoryResponse,
)
def update_category(
    category_id: int,
    category: schemas.CategoryUpdate,
    db: Session = Depends(get_db),
):
    try:
        updated_category = crud.update_category(db, category_id, category)
    except IntegrityError:
        handle_integrity_error(db)

    if updated_category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )

    return updated_category


@app.delete(
    "/categories/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
):
    try:
        deleted = crud.delete_category(db, category_id)
    except IntegrityError:
        handle_integrity_error(db)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )


# Supplier endpoints
@app.post(
    "/suppliers",
    response_model=schemas.SupplierResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_supplier(
    supplier: schemas.SupplierCreate,
    db: Session = Depends(get_db),
):
    try:
        return crud.create_supplier(db, supplier)
    except IntegrityError:
        handle_integrity_error(db)


@app.get("/suppliers", response_model=list[schemas.SupplierResponse])
def read_suppliers(db: Session = Depends(get_db)):
    return crud.get_suppliers(db)


@app.get(
    "/suppliers/{supplier_id}",
    response_model=schemas.SupplierResponse,
)
def read_supplier(
    supplier_id: int,
    db: Session = Depends(get_db),
):
    supplier = crud.get_supplier(db, supplier_id)

    if supplier is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Supplier not found",
        )

    return supplier


@app.put(
    "/suppliers/{supplier_id}",
    response_model=schemas.SupplierResponse,
)
def update_supplier(
    supplier_id: int,
    supplier: schemas.SupplierUpdate,
    db: Session = Depends(get_db),
):
    try:
        updated_supplier = crud.update_supplier(db, supplier_id, supplier)
    except IntegrityError:
        handle_integrity_error(db)

    if updated_supplier is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Supplier not found",
        )

    return updated_supplier


@app.delete(
    "/suppliers/{supplier_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_supplier(
    supplier_id: int,
    db: Session = Depends(get_db),
):
    try:
        deleted = crud.delete_supplier(db, supplier_id)
    except IntegrityError:
        handle_integrity_error(db)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Supplier not found",
        )


# Product endpoints
@app.post(
    "/products",
    response_model=schemas.ProductResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_product(
    product: schemas.ProductCreate,
    db: Session = Depends(get_db),
):
    try:
        return crud.create_product(db, product)
    except IntegrityError:
        handle_integrity_error(db)


@app.get("/products", response_model=list[schemas.ProductResponse])
def read_products(db: Session = Depends(get_db)):
    return crud.get_products(db)


@app.get(
    "/products/{product_id}",
    response_model=schemas.ProductResponse,
)
def read_product(
    product_id: int,
    db: Session = Depends(get_db),
):
    product = crud.get_product(db, product_id)

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    return product


@app.put(
    "/products/{product_id}",
    response_model=schemas.ProductResponse,
)
def update_product(
    product_id: int,
    product: schemas.ProductUpdate,
    db: Session = Depends(get_db),
):
    try:
        updated_product = crud.update_product(db, product_id, product)
    except IntegrityError:
        handle_integrity_error(db)

    if updated_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    return updated_product


@app.delete(
    "/products/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
):
    try:
        deleted = crud.delete_product(db, product_id)
    except IntegrityError:
        handle_integrity_error(db)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
