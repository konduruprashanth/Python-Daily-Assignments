from datetime import datetime
from decimal import Decimal

from pydantic import Field

from app.schemas.category import ORMBase


class ProductCreate(ORMBase):
    product_name: str = Field(min_length=1, max_length=150)
    description: str | None = None
    category_id: int = Field(gt=0)
    supplier_id: int = Field(gt=0)
    price: Decimal = Field(gt=0, max_digits=10, decimal_places=2)
    quantity: int = Field(ge=0)
    sku: str = Field(min_length=1, max_length=50)
    reorder_level: int = Field(default=10, ge=0)


class ProductUpdate(ORMBase):
    product_name: str | None = Field(default=None, min_length=1, max_length=150)
    description: str | None = None
    category_id: int | None = Field(default=None, gt=0)
    supplier_id: int | None = Field(default=None, gt=0)
    price: Decimal | None = Field(default=None, gt=0, max_digits=10, decimal_places=2)
    quantity: int | None = Field(default=None, ge=0)
    sku: str | None = Field(default=None, min_length=1, max_length=50)
    reorder_level: int | None = Field(default=None, ge=0)


class ProductResponse(ORMBase):
    product_id: int
    product_name: str
    description: str | None
    category_id: int
    supplier_id: int
    price: Decimal
    quantity: int
    sku: str
    reorder_level: int
    updated_at: datetime
    created_date: datetime
    updated_date: datetime
