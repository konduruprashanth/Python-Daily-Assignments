from pydantic import BaseModel, EmailStr, Field


class BookCreate(BaseModel):
    book_name: str
    author: str
    category: str
    isbn: str
    price: float = Field(gt=0)
    available_quantity: int = Field(ge=0)


class BookResponse(BookCreate):
    id: int

    class Config:
        from_attributes = True


class MemberCreate(BaseModel):
    member_name: str
    email: EmailStr
    phone_number: str | None = None
    membership_type: str | None = None


class MemberResponse(MemberCreate):
    id: int

    class Config:
        from_attributes = True