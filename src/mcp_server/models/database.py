from sqlmodel import SQLModel, create_engine, Session
from config.settings import settings
from typing import Generator
import os

# Create the database engine
engine = create_engine(settings.database_url, echo=False)


def get_session() -> Generator[Session, None, None]:
    """Dependency to get a database session."""
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    """Create database tables."""
    SQLModel.metadata.create_all(engine)


# For migrations and initialization
def init_db():
    """Initialize the database and create tables."""
    create_db_and_tables()