from sqlmodel import SQLModel, Field
from sqlalchemy import Column, String
from typing import Optional
from datetime import datetime
import uuid


class TaskBase(SQLModel):
    """Base class for Task with shared attributes."""

    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None)
    status: str = Field(default="pending", sa_column=Column(String, nullable=False))  # ['pending', 'in-progress', 'completed', 'cancelled']
    priority: str = Field(default="medium", sa_column=Column(String, nullable=False))
    user_id: int = Field(default=1, foreign_key="user.id")  # Foreign key linking to User, defaults to user 1
    due_date: Optional[datetime] = Field(default=None)


class Task(TaskBase, table=True):
    """Task model representing a specific work item that can be created, updated, or managed through natural language commands."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = Field(default=None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if 'created_at' not in kwargs or kwargs['created_at'] is None:
            self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()


class TaskCreate(TaskBase):
    """Schema for creating a new task."""
    due_date: Optional[datetime] = Field(default=None)


class TaskUpdate(SQLModel):
    """Schema for updating an existing task."""

    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None)
    status: Optional[str] = Field(default=None)  # ['pending', 'in-progress', 'completed', 'cancelled']
    priority: Optional[str] = Field(default=None)
    due_date: Optional[datetime] = Field(default=None)


class TaskRead(TaskBase):
    """Schema for reading task data."""

    id: str
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime]
    due_date: Optional[datetime] = Field(default=None)


class TaskStatusUpdate(SQLModel):
    """Schema for updating task status."""

    completed: bool