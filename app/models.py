"""
SQLAlchemy models for the Weather Forecasting API.

Currently defines a single `User` model for storing registered users.
Each user has a unique email address and a hashed password. Future
models (e.g. for API keys or tokens) can be added here as needed.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from .database import Base


class User(Base):
    """
    SQLAlchemy model representing a user in the database.

    Each user has a unique email and a hashed password. A timestamp column is
    not included here because existing databases created from earlier versions
    of this project may lack a `created_at` column, which would cause errors
    when querying. If you wish to track user creation times, you can add a
    `created_at` column here and recreate the database tables accordingly.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(320), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)