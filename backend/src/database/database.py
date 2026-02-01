from sqlmodel import Session, SQLModel
from typing import Generator
from ..core.database import engine  # Use the same engine as the main app
from contextlib import contextmanager

@contextmanager
def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    """Create database tables if they don't exist"""
    from ..core.database import init_db
    init_db()  # Use the same initialization as the main app