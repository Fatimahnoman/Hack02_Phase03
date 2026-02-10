from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone
from pydantic import field_validator
import uuid


class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)


class User(UserBase, table=True):
    """User model representing the chatbot user with identity and preferences."""
    id: Optional[int] = Field(default=None, primary_key=True)  # Keep as int to match existing DB
    hashed_password: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    # NOTE: preferences field is commented out to match existing DB schema
    # preferences: Optional[str] = Field(default=None)  # JSON serialized as text


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
    id: int  # Keep as int to match existing DB
    email: str
    created_at: datetime
    updated_at: datetime
    # NOTE: preferences field is commented out to match existing DB schema
    # preferences: Optional[str] = None