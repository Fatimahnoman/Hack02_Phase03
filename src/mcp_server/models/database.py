from sqlmodel import SQLModel, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine as sqlalchemy_create_engine
from config.settings import settings
from typing import Generator
import os

# Create the database engine
engine = create_engine(settings.database_url, echo=False)

# Create a configured "SessionLocal" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session() -> Generator:
    """Dependency to get a database session."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def create_db_and_tables():
    """Create database tables."""
    SQLModel.metadata.create_all(engine)


# For migrations and initialization
def init_db():
    """Initialize the database and create tables."""
    create_db_and_tables()