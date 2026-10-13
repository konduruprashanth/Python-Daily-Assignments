from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class ORMBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


# Category Schemas
class CategoryCreate(BaseModel):
    category_name: str = Field(min_length=1, max_length=100)
    description: str | None = None


class CategoryUpdate(BaseModel):
    category_name: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = None


class CategoryResponse(ORMBase):
    category_id: int
    category_name: str
    description: str | None
    created_date: datetime


# Supplier Schemas
class SupplierCreate(BaseModel):
    supplier_name: str = Field(min_length=1, max_length=150)
    email: EmailStr
    phone_number: str | None = Field(default=None, max_length=20)
    address: str | None = None
    company_name: str | None = Field(default=None, max_length=150)


class SupplierUpdate(BaseModel):
    supplier_name: str | None = Field(default=None, min_length=1, max_length=150)
    email: EmailStr | None = None
    phone_number: str | None = Field(default=None, max_length=20)
    address: str | None = None
    company_name: str | None = Field(default=None, max_length=150)


class SupplierResponse(ORMBase):
    supplier_id: int
    supplier_name: str
    email: EmailStr
    phone_number: str | None
    address: str | None
    company_name: str | None
    created_date: datetime


# Product Schemas
class ProductCreate(BaseModel):
    product_name: str = Field(min_length=1, max_length=150)
    description: str | None = None
    category_id: int = Field(gt=0)
    supplier_id: int = Field(gt=0)
    price: Decimal = Field(gt=0, max_digits=10, decimal_places=2)
    quantity: int = Field(ge=0)


class ProductUpdate(BaseModel):
    product_name: str | None = Field(default=None, min_length=1, max_length=150)
    description: str | None = None
    category_id: int | None = Field(default=None, gt=0)
    supplier_id: int | None = Field(default=None, gt=0)
    price: Decimal | None = Field(default=None, gt=0, max_digits=10, decimal_places=2)
    quantity: int | None = Field(default=None, ge=0)


class ProductResponse(ORMBase):
    product_id: int
    product_name: str
    description: str | None
    category_id: int
    supplier_id: int
    price: Decimal
    quantity: int
    created_date: datetime
    updated_date: datetime
