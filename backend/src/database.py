"""
Database module for handling SQLModel database connections and engine setup.
"""
from sqlmodel import create_engine, Session, SQLModel
from typing import Generator
from contextlib import contextmanager
from .core.config import settings

import urllib.parse

# Determine if we're using SQLite or PostgreSQL to set appropriate connection parameters
parsed_url = urllib.parse.urlparse(settings.database_url)
is_sqlite = parsed_url.scheme.lower() == 'sqlite'

if is_sqlite:
    # SQLite doesn't support connection pooling or many other parameters
    engine = create_engine(
        settings.database_url,
        echo=settings.database_echo
    )
else:
    # Create the database engine with proper connection pooling for Neon Serverless PostgreSQL
    engine = create_engine(
        settings.database_url,
        echo=settings.database_echo,
        pool_size=5,
        max_overflow=10,
        pool_timeout=30,
        pool_pre_ping=True,  # Verify connections before use
        pool_recycle=300,  # Recycle connections
        connect_args={
            "connect_timeout": 10,
        }
    )


def create_db_and_tables():
    """
    Create database tables based on SQLModel models.
    """
    SQLModel.metadata.create_all(engine)


@contextmanager
def get_session_context() -> Generator[Session, None, None]:
    """
    Context manager for getting a database session.
    Handles session lifecycle automatically.
    """
    session = Session(engine)
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()