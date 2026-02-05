"""Conversation Context model for stateless chatbot operations."""

from datetime import datetime, timedelta
from typing import Optional
from sqlmodel import Field, SQLModel
import uuid


class ConversationContextBase(SQLModel):
    """Base model for ConversationContext containing shared attributes."""
    user_id: str = Field(foreign_key="user.id")  # Foreign key linking to User
    context_type: str = Field(sa_column_kwargs={"nullable": False})  # ['task-assist', 'general-chat', 'follow-up', 'custom']
    context_data: Optional[str] = Field(default=None)  # JSON serialized as text
    expires_at: datetime = Field(sa_column_kwargs={"nullable": False})  # Expiration timestamp


class ConversationContext(ConversationContextBase, table=True):
    """ConversationContext model storing necessary conversation context in the database for stateless operation."""

    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if 'id' not in kwargs or kwargs['id'] is None:
            self.id = str(uuid.uuid4())
        if 'created_at' not in kwargs or kwargs['created_at'] is None:
            self.created_at = datetime.utcnow()
        # Set expires_at if not provided, default to 24 hours from creation
        if 'expires_at' not in kwargs or kwargs['expires_at'] is None:
            self.expires_at = datetime.utcnow() + timedelta(hours=24)


class ConversationContextCreate(ConversationContextBase):
    """Schema for creating a new conversation context."""
    pass


class ConversationContextRead(ConversationContextBase):
    """Schema for reading conversation context data."""
    id: str
    created_at: datetime