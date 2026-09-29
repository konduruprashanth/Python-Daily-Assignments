from pydantic import BaseModel


class Student(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    age: int
    course: str
    address: str | None = None