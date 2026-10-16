from datetime import datetime

from pydantic import EmailStr, Field

from app.schemas.category import ORMBase


class SupplierCreate(ORMBase):
    supplier_name: str = Field(min_length=1, max_length=150)
    email: EmailStr
    phone_number: str | None = Field(default=None, max_length=20)
    phone: str | None = Field(default=None, max_length=20)
    address: str | None = None
    company_name: str | None = Field(default=None, max_length=150)
    is_active: bool = True


class SupplierUpdate(ORMBase):
    supplier_name: str | None = Field(
        default=None, min_length=1, max_length=150
    )
    email: EmailStr | None = None
    phone_number: str | None = Field(default=None, max_length=20)
    phone: str | None = Field(default=None, max_length=20)
    address: str | None = None
    company_name: str | None = Field(default=None, max_length=150)
    is_active: bool | None = None


class SupplierResponse(ORMBase):
    supplier_id: int
    supplier_name: str
    email: EmailStr
    phone_number: str | None
    phone: str | None
    address: str | None
    company_name: str | None
    is_active: bool
    created_date: datetime