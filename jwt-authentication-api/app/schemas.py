from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    full_name: str = Field(..., min_length=2)
    email: EmailStr
    password: str = Field(..., min_length=6)
    role: str = "User"


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    role: str
    created_date: datetime

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    status: str = "Pending"
    priority: str = "Medium"
    assigned_to: Optional[int] = None
    due_date: datetime


class TaskUpdate(BaseModel):
    title: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    status: str
    priority: str
    due_date: datetime


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    status: str
    priority: str
    assigned_to: int
    created_date: datetime
    due_date: datetime

    class Config:
        from_attributes = True