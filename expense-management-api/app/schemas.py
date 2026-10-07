from datetime import date, datetime
from enum import Enum

from pydantic import BaseModel, Field


class PaymentMethod(str, Enum):
    CASH = "Cash"
    CARD = "Card"
    UPI = "UPI"
    BANK_TRANSFER = "Bank Transfer"


class ExpenseStatus(str, Enum):
    PENDING = "Pending"
    APPROVED = "Approved"
    REJECTED = "Rejected"


class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)


class CategoryCreate(CategoryBase):
    pass


class CategoryResponse(CategoryBase):
    id: int

    model_config = {"from_attributes": True}


class ExpenseBase(BaseModel):
    employee_name: str = Field(..., min_length=1)
    category_id: int
    amount: float = Field(..., gt=0)
    description: str = Field(..., min_length=1)
    expense_date: date
    payment_method: PaymentMethod
    status: ExpenseStatus


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseResponse(ExpenseBase):
    id: int
    created_date: datetime

    model_config = {"from_attributes": True}