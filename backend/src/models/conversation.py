from sqlmodel import SQLModel, Field
from sqlalchemy import Column, String, JSON
from typing import Optional
from datetime import datetime
import uuid


class Conversation(SQLModel, table=True):
    """Conversation model representing a sequence of messages between a user and the agent, stored in the database with timestamps and metadata."""

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    conversation_metadata: Optional[dict] = Field(default=None, sa_column=Column(JSON, nullable=True))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ConversationCreate(SQLModel):
    """Schema for creating a new conversation."""

    conversation_metadata: Optional[dict] = None


class ConversationUpdate(SQLModel):
    """Schema for updating an existing conversation."""

    conversation_metadata: Optional[dict] = None


class ConversationRead(SQLModel):
    """Schema for reading conversation data."""

    id: uuid.UUID
    conversation_metadata: Optional[dict] = None
    created_at: datetime
    updated_at: datetime