from sqlmodel import SQLModel, Field
from sqlalchemy import Column, String, JSON
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum
import uuid


class MessageRole(str, Enum):
    """
    Enum for message roles (sender types).
    """
    user = "user"
    assistant = "assistant"
    system = "system"
    tool = "tool"


class MessageBase(SQLModel):
    """Base class for Message with shared attributes."""

    conversation_id: uuid.UUID = Field(foreign_key="conversation.id")
    role: str = Field(sa_column=Column(String, nullable=False))  # "user", "assistant", "system", "tool"
    content: str = Field(sa_column=Column(String, nullable=False))
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    tool_call_id: Optional[uuid.UUID] = Field(default=None, foreign_key="toolcall.id")


class Message(MessageBase, table=True):
    """Message model representing an individual message within a conversation."""

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    conversation_id: uuid.UUID = Field(foreign_key="conversation.id")
    role: str = Field(sa_column=Column(String, nullable=False))  # "user", "assistant", "system", "tool"
    content: str = Field(sa_column=Column(String, nullable=False))
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    tool_call_id: Optional[uuid.UUID] = Field(default=None, foreign_key="toolcall.id")


class MessageCreate(SQLModel):
    """Schema for creating a new message."""

    conversation_id: uuid.UUID
    role: str  # "user", "assistant", "system", "tool"
    content: str
    tool_call_id: Optional[uuid.UUID] = None


class MessageUpdate(SQLModel):
    """Schema for updating an existing message."""

    content: Optional[str] = None
    role: Optional[str] = None


class MessageRead(MessageBase):
    """Schema for reading message data."""

    id: uuid.UUID
    timestamp: datetime