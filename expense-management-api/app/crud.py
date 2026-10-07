from datetime import date, datetime

from sqlalchemy import func
from sqlalchemy.orm import Session

from . import models, schemas


# -------------------------
# Category CRUD
# -------------------------

def create_category(db: Session, category: schemas.CategoryCreate):
    existing_category = (
        db.query(models.Category)
        .filter(models.Category.name == category.name)
        .first()
    )

    if existing_category:
        return None

    db_category = models.Category(
        name=category.name,
        description=category.description,
    )

    db.add(db_category)
    db.commit()
    db.refresh(db_category)

    return db_category


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
    category: schemas.CategoryCreate,
):
    db_category = get_category(db, category_id)

    if not db_category:
        return None

    duplicate_category = (
        db.query(models.Category)
        .filter(
            models.Category.name == category.name,
            models.Category.id != category_id,
        )
        .first()
    )

    if duplicate_category:
        return "duplicate"

    db_category.name = category.name
    db_category.description = category.description

    db.commit()
    db.refresh(db_category)

    return db_category


def delete_category(db: Session, category_id: int):
    db_category = get_category(db, category_id)

    if not db_category:
        return None

    db.delete(db_category)
    db.commit()

    return db_category


# -------------------------
# Expense CRUD
# -------------------------

def create_expense(db: Session, expense: schemas.ExpenseCreate):
    category = get_category(db, expense.category_id)

    if not category:
        return None

    db_expense = models.Expense(
        employee_name=expense.employee_name,
        category_id=expense.category_id,
        amount=expense.amount,
        description=expense.description,
        expense_date=expense.expense_date,
        payment_method=expense.payment_method.value,
        status=expense.status.value,
    )

    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)

    return db_expense


def get_expenses(
    db: Session,
    category_id: int | None = None,
    status: schemas.ExpenseStatus | None = None,
    payment_method: schemas.PaymentMethod | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
):
    query = db.query(models.Expense)

    if category_id is not None:
        query = query.filter(models.Expense.category_id == category_id)

    if status is not None:
        query = query.filter(models.Expense.status == status.value)

    if payment_method is not None:
        query = query.filter(
            models.Expense.payment_method == payment_method.value
        )

    if start_date is not None:
        query = query.filter(models.Expense.expense_date >= start_date)

    if end_date is not None:
        query = query.filter(models.Expense.expense_date <= end_date)

    return query.all()


def get_expense(db: Session, expense_id: int):
    return (
        db.query(models.Expense)
        .filter(models.Expense.id == expense_id)
        .first()
    )


def update_expense(
    db: Session,
    expense_id: int,
    expense: schemas.ExpenseCreate,
):
    db_expense = get_expense(db, expense_id)

    if not db_expense:
        return None

    category = get_category(db, expense.category_id)

    if not category:
        return "category_not_found"

    db_expense.employee_name = expense.employee_name
    db_expense.category_id = expense.category_id
    db_expense.amount = expense.amount
    db_expense.description = expense.description
    db_expense.expense_date = expense.expense_date
    db_expense.payment_method = expense.payment_method.value
    db_expense.status = expense.status.value

    db.commit()
    db.refresh(db_expense)

    return db_expense


def delete_expense(db: Session, expense_id: int):
    db_expense = get_expense(db, expense_id)

    if not db_expense:
        return None

    db.delete(db_expense)
    db.commit()

    return db_expense


def get_total_expenses(db: Session):
    total = db.query(func.sum(models.Expense.amount)).scalar()

    return total or 0