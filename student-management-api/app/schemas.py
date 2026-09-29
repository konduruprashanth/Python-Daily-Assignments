from pydantic import BaseModel, EmailStr, Field


class StudentCreate(BaseModel):
    id: int
    name: str = Field(min_length=1)
    email: EmailStr
    phone: str = Field(
        min_length=10,
        max_length=15,
        pattern=r"^\d{10, 15}$"
    )
    age: int = Field(ge=18, le=60)
    course: str = Field(min_length=1)
    address: str | None = None


class StudentResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: str
    age: int
    course: str
    address: str | None = None

    model_config = {
        "from_attributes": True
    }
    