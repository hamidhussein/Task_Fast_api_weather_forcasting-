from app.database import engine
from app.models import Base


def main() -> None:
    """Initialize the database by creating tables."""
    Base.metadata.create_all(bind=engine)
    print("Database initialized.")


if __name__ == "__main__":
    main()