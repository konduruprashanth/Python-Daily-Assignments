from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import engine, get_db, Base
from app import models, schemas, crud


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Product Inventory Management API",
    description="Manage product inventory and categories using FastAPI and SQLAlchemy.",
    version="1.0.0",
)


# ---------------- CATEGORY APIs ----------------

@app.post(
    "/categories",
    response_model=schemas.CategoryResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_category(
    category: schemas.CategoryCreate,
    db: Session = Depends(get_db),
):
    result = crud.create_category(db, category)

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Category name already exists",
        )

    return result


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
    result = crud.update_category(db, category_id, category)

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )

    if result == "duplicate":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Category name already exists",
        )

    return result


@app.delete(
    "/categories/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
):
    result = crud.delete_category(db, category_id)

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )

    if result == "has_products":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot delete a category that contains products",
        )


# ---------------- PRODUCT APIs ----------------

@app.post(
    "/products",
    response_model=schemas.ProductResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_product(
    product: schemas.ProductCreate,
    db: Session = Depends(get_db),
):
    result = crud.create_product(db, product)

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category does not exist",
        )

    return result


@app.get("/products", response_model=list[schemas.ProductResponse])
def read_products(
    category_id: int | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    search: str | None = None,
    db: Session = Depends(get_db),
):
    if category_id is not None and category_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="category_id must be greater than 0",
        )

    if min_price is not None and min_price < 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="min_price cannot be negative",
        )

    if max_price is not None and max_price < 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="max_price cannot be negative",
        )

    if (
        min_price is not None
        and max_price is not None
        and min_price > max_price
    ):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="min_price cannot be greater than max_price",
        )

    return crud.get_products(
        db,
        category_id=category_id,
        min_price=min_price,
        max_price=max_price,
        search=search,
    )


@app.get(
    "/products/inventory-value",
    response_model=dict[str, float],
)
def read_inventory_value(db: Session = Depends(get_db)):
    return {"inventory_value": crud.get_inventory_value(db)}


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
    result = crud.update_product(db, product_id, product)

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    if result == "invalid_category":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category does not exist",
        )

    return result


@app.delete(
    "/products/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
):
    result = crud.delete_product(db, product_id)

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )


@app.get(
    "/categories/{category_id}/products",
    response_model=list[schemas.ProductResponse],
)
def read_category_products(
    category_id: int,
    db: Session = Depends(get_db),
):
    category = crud.get_category(db, category_id)

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )

    return crud.get_category_products(db, category_id)