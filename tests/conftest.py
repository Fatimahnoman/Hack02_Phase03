import pytest
from sqlmodel import create_engine, Session
from sqlmodel.pool import StaticPool
from typing import Generator

# Import models for table creation
from src.mcp_server.models.task import Task

@pytest.fixture(name="engine")
def fixture_engine():
    # Use in-memory SQLite for testing
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    # Create tables
    from src.mcp_server.models.database import SQLModel
    SQLModel.metadata.create_all(bind=engine)

    yield engine

    # Cleanup after tests
    engine.dispose()


@pytest.fixture(name="session")
def fixture_session(engine) -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session