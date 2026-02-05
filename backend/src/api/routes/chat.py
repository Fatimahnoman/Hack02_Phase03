"""Chat endpoint for the stateless conversation cycle."""

from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any, Optional
from sqlmodel import Session
from ...core.database import get_session_context
from ...services.stateless_conversation_service import StatelessConversationService
from ...services.database_service import DatabaseService
from ...services.intent_parser import parse_intent
from pydantic import BaseModel
from datetime import datetime
import uuid


router = APIRouter(prefix="/chat", tags=["chat"])


class ChatRequest(BaseModel):
    """Request model for chat interactions."""
    user_input: str
    user_id: str
    session_metadata: Optional[Dict[str, Any]] = None


class ChatResponse(BaseModel):
    """Response model for chat interactions."""
    response: str
    intent: str
    state_reflection: Dict[str, Any]
    tool_execution_result: Optional[Dict[str, Any]] = None
    timestamp: str


@router.post("/", response_model=ChatResponse)
async def process_chat_message(
    request: ChatRequest,
    session: Session = Depends(get_session_context)
) -> ChatResponse:
    """
    Process a chat message in a stateless manner.

    Processes a user message without relying on conversation history.
    Each request is handled independently using only current input and database state.
    """
    try:
        # Create service instances
        db_service = DatabaseService(session)
        conversation_service = StatelessConversationService(db_service)

        # Process the chat request statelessly with tool execution tracking
        result = await conversation_service.process_request_with_tool_execution(
            user_input=request.user_input,
            user_id=request.user_id,
            session_metadata=request.session_metadata
        )

        # Prepare the response
        response = ChatResponse(
            response=result.get("response", "I processed your request."),
            intent=result.get("intent", "unknown"),
            state_reflection=result.get("state_reflection", {}),
            tool_execution_result=result.get("tool_execution_result"),
            timestamp=datetime.utcnow().isoformat()
        )

        return response

    except Exception as e:
        # Handle any errors gracefully
        error_response = ChatResponse(
            response=f"I encountered an error: {str(e)}",
            intent="error",
            state_reflection={},
            timestamp=datetime.utcnow().isoformat()
        )
        return error_response


@router.get("/health")
async def chat_health() -> Dict[str, str]:
    """Health check endpoint for the chat service."""
    return {"status": "healthy", "service": "chat", "timestamp": datetime.utcnow().isoformat()}