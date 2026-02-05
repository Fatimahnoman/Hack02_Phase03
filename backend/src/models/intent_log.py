"""Intent Log model for tracking user intents in stateless chatbot operations."""

from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel
import uuid


class IntentLogBase(SQLModel):
    """Base model for IntentLog containing shared attributes."""
    user_id: str = Field(foreign_key="user.id")  # Foreign key linking to User
    input_text: str = Field(sa_column_kwargs={"nullable": False})  # Original user input
    detected_intent: str = Field(sa_column_kwargs={"nullable": False})  # Classified intent from the input
    extracted_parameters: Optional[str] = Field(default=None)  # JSON serialized parameters
    session_id: Optional[str] = Field(default=None)  # Identifier for the session (for grouping related requests)


class IntentLog(IntentLogBase, table=True):
    """IntentLog model recording all parsed intents for audit, debugging, and consistency verification."""

    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    processed_at: datetime = Field(default_factory=datetime.utcnow)  # Timestamp when intent was processed

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if 'id' not in kwargs or kwargs['id'] is None:
            self.id = str(uuid.uuid4())
        if 'processed_at' not in kwargs or kwargs['processed_at'] is None:
            self.processed_at = datetime.utcnow()


class IntentLogCreate(IntentLogBase):
    """Schema for creating a new intent log entry."""
    pass


class IntentLogRead(IntentLogBase):
    """Schema for reading intent log data."""
    id: str
    processed_at: datetime