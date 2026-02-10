"""Chat endpoint for the stateless conversation cycle."""

from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any, Optional
from sqlmodel import Session
from ...core.database import get_session_context
from ...services.stateless_conversation_service import StatelessConversationService
from ...services.database_service import DatabaseService
from pydantic import BaseModel
from datetime import datetime


router = APIRouter(prefix="/chat", tags=["chat"])


class ChatRequest(BaseModel):
    """Request model for chat interactions."""
    user_input: str
    user_id: Optional[str] = None  # Make user_id optional
    session_metadata: Optional[Dict[str, Any]] = None


class ChatResponse(BaseModel):
    """Response model for chat interactions."""
    response: str
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

        # Process the chat request statelessly
        result = await conversation_service.process_request(
            user_input=request.user_input,
            user_id=request.user_id,
            session_metadata=request.session_metadata
        )

        # Prepare the response
        response = ChatResponse(
            response=result.get("response", "I processed your request."),
            state_reflection=result.get("state_reflection", {}),
            tool_execution_result=result.get("tool_execution_result"),
            timestamp=datetime.utcnow().isoformat()
        )

        return response

    except Exception as e:
        # Handle any errors gracefully with a user-friendly message
        # Make sure API errors are not confused with authentication errors
        import traceback
        error_msg = str(e)
        print(f"Error in chat endpoint: {e}")
        
        # Check if this is an API-related error that shouldn't be treated as auth error
        if "401" in error_msg or "Unauthorized" in error_msg or "User not found" in error_msg:
            # This is an API error, not a user authentication error
            error_response = ChatResponse(
                response="I'm sorry, I encountered an issue with the AI service. Please try again later.",
                state_reflection={},
                timestamp=datetime.utcnow().isoformat()
            )
        else:
            print(traceback.format_exc())  # For debugging
            error_response = ChatResponse(
                response="I'm sorry, I encountered an issue processing your request. Please try again.",
                state_reflection={},
                timestamp=datetime.utcnow().isoformat()
            )
        
        return error_response


@router.get("/health")
async def chat_health() -> Dict[str, str]:
    """Health check endpoint for the chat service."""
    return {"status": "healthy", "service": "chat", "timestamp": datetime.utcnow().isoformat()}
