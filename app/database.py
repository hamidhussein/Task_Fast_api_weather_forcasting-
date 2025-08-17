"""
Database setup for the Weather Forecasting API.

This module defines the SQLAlchemy engine and session factory used throughout
the application. It pulls configuration from `app.config.settings` and
exposes a dependency to provide a session per request. All database
connections are automatically closed after use.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from .config import settings


class Base(DeclarativeBase):
    """Base class for declarative models."""
    pass


# Create the SQLAlchemy engine using the assembled URL from settings
engine = create_engine(settings.database.sqlalchemy_url, echo=False, future=True)


# Session factory used as a dependency in FastAPI endpoints
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


def get_db():
    """Yield a database session and ensure it is closed after use."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()