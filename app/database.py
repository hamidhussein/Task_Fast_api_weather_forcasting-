from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from .config import settings

class Base(DeclarativeBase):
    """
    Declarative base class for SQLAlchemy models.
    """
    pass

# Assemble the SQLAlchemy database URL for PostgreSQL
SQLALCHEMY_DATABASE_URL = (
    f"postgresql+psycopg2://{settings.database.database_user}:"  # Accessing the database user via settings.database
    f"{settings.database.database_password}@"                  # Accessing the database password via settings.database
    f"{settings.database.database_host}:{settings.database.database_port}/"
    f"{settings.database.database_name}"                        # Accessing the database name via settings.database
)

# Create the SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True, future=True)

# Create a session factory
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)

def get_db():
    """
    Dependency that yields a database session and ensures it is closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
