from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    phone_number = Column(String, nullable=True)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False, default="User")
    created_date = Column(DateTime, default=datetime.utcnow)