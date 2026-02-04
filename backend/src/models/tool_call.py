from sqlmodel import SQLModel, Field
from sqlalchemy import Column, String, JSON
from typing import Optional, Dict, Any
from datetime import datetime
import uuid


class ToolCallBase(SQLModel):
    """Base class for ToolCall with shared attributes."""

    function_name: str = Field(sa_column=Column(String, nullable=False))
    parameters: Dict[str, Any] = Field(sa_column=Column(JSON, nullable=False))
    result: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(JSON, nullable=True))
    status: str = Field(sa_column=Column(String, nullable=False))  # "success", "error", "pending"
    entity_id: Optional[str] = Field(default=None)
    entity_type: Optional[str] = Field(default=None, sa_column=Column(String, nullable=True))


class ToolCall(ToolCallBase, table=True):
    """ToolCall model representing an invocation of an MCP tool with parameters and results, logged for auditing purposes."""

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = Field(default=None)


class ToolCallCreate(SQLModel):
    """Schema for creating a new tool call."""

    function_name: str
    parameters: dict
    entity_id: Optional[str] = None
    entity_type: Optional[str] = None


class ToolCallUpdate(SQLModel):
    """Schema for updating an existing tool call."""

    result: Optional[dict] = None
    status: Optional[str] = None
    completed_at: Optional[datetime] = None


class ToolCallRead(ToolCallBase):
    """Schema for reading tool call data."""

    id: uuid.UUID
    created_at: datetime
    completed_at: Optional[datetime]