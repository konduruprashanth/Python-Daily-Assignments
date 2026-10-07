from datetime import date

from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlalchemy.orm import Session

from . import crud, schemas
from .database import Base, engine, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Expense Management API")


# -------------------------
# Category APIs
# -------------------------

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
            status_code=409,
            detail="Category name already exists",
        )

    return result


@app.get(
    "/categories",
    response_model=list[schemas.CategoryResponse],
)
def get_categories(db: Session = Depends(get_db)):
    return crud.get_categories(db)


@app.get(
    "/categories/{category_id}",
    response_model=schemas.CategoryResponse,
)
def get_category(
    category_id: int,
    db: Session = Depends(get_db),
):
    category = crud.get_category(db, category_id)

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found",
        )

    return category


@app.put(
    "/categories/{category_id}",
    response_model=schemas.CategoryResponse,
)
def update_category(
    category_id: int,
    category: schemas.CategoryCreate,
    db: Session = Depends(get_db),
):
    result = crud.update_category(db, category_id, category)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Category not found",
        )

    if result == "duplicate":
        raise HTTPException(
            status_code=409,
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
    category = crud.delete_category(db, category_id)

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found",
        )

    return None


# -------------------------
# Expense APIs
# -------------------------

@app.post(
    "/expenses",
    response_model=schemas.ExpenseResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_expense(
    expense: schemas.ExpenseCreate,
    db: Session = Depends(get_db),
):
    result = crud.create_expense(db, expense)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Category not found",
        )

    return result


@app.get(
    "/expenses",
    response_model=list[schemas.ExpenseResponse],
)
def get_expenses(
    category_id: int | None = Query(default=None),
    status_filter: schemas.ExpenseStatus | None = Query(
        default=None,
        alias="status",
    ),
    payment_method: schemas.PaymentMethod | None = Query(default=None),
    start_date: date | None = Query(default=None),
    end_date: date | None = Query(default=None),
    db: Session = Depends(get_db),
):
    if start_date and end_date and start_date > end_date:
        raise HTTPException(
            status_code=400,
            detail="start_date cannot be after end_date",
        )

    return crud.get_expenses(
        db,
        category_id=category_id,
        status=status_filter,
        payment_method=payment_method,
        start_date=start_date,
        end_date=end_date,
    )


# -------------------------
# Total Expenses API
# -------------------------

# This must come BEFORE /expenses/{expense_id}
@app.get("/expenses/total")
def get_total_expenses(db: Session = Depends(get_db)):
    total = crud.get_total_expenses(db)

    return {
        "total_expenses": total,
    }


@app.get(
    "/expenses/{expense_id}",
    response_model=schemas.ExpenseResponse,
)
def get_expense(
    expense_id: int,
    db: Session = Depends(get_db),
):
    expense = crud.get_expense(db, expense_id)

    if not expense:
        raise HTTPException(
            status_code=404,
            detail="Expense not found",
        )

    return expense


@app.put(
    "/expenses/{expense_id}",
    response_model=schemas.ExpenseResponse,
)
def update_expense(
    expense_id: int,
    expense: schemas.ExpenseCreate,
    db: Session = Depends(get_db),
):
    result = crud.update_expense(db, expense_id, expense)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Expense not found",
        )

    if result == "category_not_found":
        raise HTTPException(
            status_code=404,
            detail="Category not found",
        )

    return result


@app.delete(
    "/expenses/{expense_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_expense(
    expense_id: int,
    db: Session = Depends(get_db),
):
    expense = crud.delete_expense(db, expense_id)

    if not expense:
        raise HTTPException(
            status_code=404,
            detail="Expense not found",
        )

    return None