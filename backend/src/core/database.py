from sqlmodel import SQLModel, create_engine, Session
from contextlib import contextmanager
from typing import Generator
from .config import settings
import os
from sqlalchemy.pool import QueuePool


# Create the database engine with connection pooling for PostgreSQL
connect_args = {"check_same_thread": False} if "sqlite" in settings.database_url else {}

# For PostgreSQL (especially Neon), configure connection pooling
if "postgresql" in settings.database_url:
    engine = create_engine(
        settings.database_url,
        echo=settings.database_echo,
        poolclass=QueuePool,
        pool_size=10,          # Number of connections to maintain
        max_overflow=20,       # Additional connections beyond pool_size
        pool_pre_ping=True,    # Verify connections before use
        pool_recycle=300,      # Recycle connections after 5 minutes
        connect_args=connect_args
    )
else:
    # For SQLite, use the simpler configuration
    engine = create_engine(
        settings.database_url,
        echo=settings.database_echo,
        connect_args=connect_args
    )


def init_db():
    """Initialize the database by creating all tables."""
    print("Creating database tables...")
    SQLModel.metadata.create_all(bind=engine)
    print("Database tables created successfully.")


@contextmanager
def get_session() -> Generator[Session, None, None]:
    """Provide a transactional scope around a series of operations."""
    session = Session(engine)
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


from fastapi import Depends


def get_session_context():
    """Dependency injection for FastAPI to provide database session."""
    session = Session(engine)
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        # Log the exception for debugging
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Database session error: {e}")
        raise
    finally:
        session.close()