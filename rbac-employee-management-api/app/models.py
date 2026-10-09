from datetime import datetime

from sqlalchemy import (
    Column,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(20), default="Employee", nullable=False)
    created_date = Column(DateTime, default=datetime.utcnow, nullable=False)

    employee = relationship(
        "Employee",
        back_populates="user",
        uselist=False,
    )


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        unique=True,
        nullable=False,
    )
    employee_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    phone_number = Column(String(20), nullable=False)
    department = Column(String(100), nullable=False)
    designation = Column(String(100), nullable=False)
    salary = Column(Float, nullable=False)
    joining_date = Column(Date, nullable=False)
    created_date = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship(
        "User",
        back_populates="employee",
    )