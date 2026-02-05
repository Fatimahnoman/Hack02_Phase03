"""Dependency injection module for API dependencies."""

from sqlmodel import Session
from fastapi import Depends
from ..db import get_session
from ..services.database_service import DatabaseService
from ..services.conversation_service import ConversationService


def get_database_service(session: Session = Depends(get_session)) -> DatabaseService:
    """Get a database service instance."""
    return DatabaseService(session)


def get_conversation_service(db_service: DatabaseService = Depends(get_database_service)) -> ConversationService:
    """Get a conversation service instance."""
    return ConversationService(db_service)