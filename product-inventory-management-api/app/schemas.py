from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class CategoryCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str | None = None


class CategoryUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = None


class CategoryResponse(BaseModel):
    id: int
    name: str
    description: str | None
    created_date: datetime

    model_config = ConfigDict(from_attributes=True)


class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str | None = None
    category_id: int = Field(..., gt=0)
    price: float = Field(..., gt=0)
    quantity: int = Field(..., ge=0)


class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = None
    category_id: int | None = Field(default=None, gt=0)
    price: float | None = Field(default=None, gt=0)
    quantity: int | None = Field(default=None, ge=0)


class ProductResponse(BaseModel):
    id: int
    name: str
    description: str | None
    category_id: int
    price: float
    quantity: int
    created_date: datetime
    updated_date: datetime

    model_config = ConfigDict(from_attributes=True)