from sqlalchemy import Column, Integer, String
from .database import Base


class User(Base):
    """
    SQLAlchemy model representing a user in the database.
    Each user has a unique email and a hashed password.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)