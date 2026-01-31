from sqlmodel import SQLModel, Field
from sqlalchemy import Column, String
from typing import Optional
from datetime import datetime
import uuid


class TaskBase(SQLModel):
    """Base class for Task with shared attributes."""

    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None)
    status: str = Field(default="pending", sa_column=Column(String, nullable=False))
    priority: str = Field(default="medium", sa_column=Column(String, nullable=False))


class Task(TaskBase, table=True):
    """Task model representing a specific work item that can be created, updated, or managed through natural language commands."""

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = Field(default=None)


class TaskCreate(TaskBase):
    """Schema for creating a new task."""
    pass


class TaskUpdate(SQLModel):
    """Schema for updating an existing task."""

    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None)
    status: Optional[str] = Field(default=None)
    priority: Optional[str] = Field(default=None)


class TaskRead(TaskBase):
    """Schema for reading task data."""

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime]