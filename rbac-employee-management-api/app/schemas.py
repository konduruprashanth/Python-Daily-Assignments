from datetime import date, datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class UserRole(str, Enum):
    ADMIN = "Admin"
    MANAGER = "Manager"
    EMPLOYEE = "Employee"


class UserRegister(BaseModel):
    full_name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    role: UserRole
    created_date: datetime

    model_config = ConfigDict(from_attributes=True)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class EmployeeCreate(BaseModel):
    user_id: int = Field(gt=0)
    employee_name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    phone_number: str = Field(min_length=10, max_length=10)
    department: str = Field(min_length=2, max_length=100)
    designation: str = Field(min_length=2, max_length=100)
    salary: float = Field(gt=0, allow_inf_nan=False)
    joining_date: date


class EmployeeUpdate(BaseModel):
    employee_name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    phone_number: str = Field(min_length=10, max_length=10)
    department: str = Field(min_length=2, max_length=100)
    designation: str = Field(min_length=2, max_length=100)
    salary: float = Field(gt=0, allow_inf_nan=False)
    joining_date: date


class EmployeeResponse(BaseModel):
    id: int
    user_id: int
    employee_name: str
    email: EmailStr
    phone_number: str
    department: str
    designation: str
    salary: float
    joining_date: date
    created_date: datetime

    model_config = ConfigDict(from_attributes=True)


class PhoneUpdate(BaseModel):
    phone_number: str = Field(min_length=10, max_length=10)


class RoleUpdate(BaseModel):
    role: UserRole