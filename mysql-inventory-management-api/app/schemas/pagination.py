from pydantic import BaseModel, Field

from app.schemas.product import ProductResponse


class PaginationParams(BaseModel):
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=10, ge=1, le=100)


class PaginationMetadata(BaseModel):
    total: int
    page: int
    page_size: int
    total_pages: int


class PaginatedProductResponse(PaginationMetadata):
    items: list[ProductResponse]