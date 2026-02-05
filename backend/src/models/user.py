from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone
from pydantic import field_validator
import uuid


class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)


class User(UserBase, table=True):
    """User model representing the chatbot user with identity and preferences."""
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    preferences: Optional[str] = Field(default=None)  # JSON serialized as text

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if 'id' not in kwargs or kwargs['id'] is None:
            self.id = str(uuid.uuid4())
        if 'created_at' not in kwargs or kwargs['created_at'] is None:
            self.created_at = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)


class UserCreate(UserBase):
    email: str
    password: str

    @field_validator('password')
    @classmethod
    def validate_password_length(cls, v):
        if len(v) > 72:
            raise ValueError('Password must not exceed 72 characters for security reasons')
        return v


class UserRead(SQLModel):
    id: str
    email: str
    created_at: datetime
    updated_at: datetime
    preferences: Optional[str] = None