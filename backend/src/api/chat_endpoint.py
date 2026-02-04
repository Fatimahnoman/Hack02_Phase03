from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any
from sqlmodel import Session
from ..core.database import get_session_context
from ..models.user import User
from ..services.agent_service import AgentService
from ..services.conversation_service import ConversationService
from ..services.auth_service import get_current_user
from pydantic import BaseModel
from uuid import UUID
import json


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    message: str
    conversation_id: str = None  # Optional conversation ID


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    response: str
    conversation_id: str
    tool_calls: list = []
    timestamp: str = None


router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session_context)
) -> ChatResponse:
    """
    Chat endpoint that processes natural language input through an OpenAI agent
    that interacts with MCP tools to manage tasks.
    """
    try:
        # Initialize services
        conversation_service = ConversationService(session)
        agent_service = AgentService(session)

        # Handle conversation creation or retrieval
        conversation_id = None
        if request.conversation_id:
            # Try to get existing conversation
            conversation = conversation_service.get_conversation(UUID(request.conversation_id))
            if not conversation:
                raise HTTPException(status_code=404, detail="Conversation not found")
            conversation_id = UUID(request.conversation_id)
        else:
            # Create a new conversation
            from ..models.conversation import ConversationCreate
            conversation_data = ConversationCreate(conversation_metadata={})
            conversation = conversation_service.create_conversation(conversation_data, str(current_user.id))
            conversation_id = conversation.id

        # Get conversation history for agent context
        # Only include user and assistant messages, excluding tool messages
        conversation_history = conversation_service.get_conversation_history(conversation_id)

        # Format history for agent (role and content only)
        history_for_agent = []
        for msg in conversation_history:
            # Only include user and assistant messages in the conversation history
            # Tool messages should not be part of the persistent conversation history
            if msg.role in ["user", "assistant"]:
                history_for_agent.append({
                    "role": msg.role,
                    "content": msg.content
                })

        # Process the request through the agent
        result = agent_service.process_request(request.message, history_for_agent)

        # Explicitly commit any changes made by tools before continuing
        session.commit()

        # Add user message to conversation
        from ..models.message import MessageCreate, MessageRole
        user_message = MessageCreate(
            conversation_id=conversation_id,
            role="user",
            content=request.message
        )
        conversation_service.add_message(user_message)

        # Add assistant response to conversation
        assistant_message = MessageCreate(
            conversation_id=conversation_id,
            role="assistant",
            content=result.get("response", "")
        )
        conversation_service.add_message(assistant_message)

        # Commit the conversation messages
        session.commit()

        # Import datetime for timestamp
        from datetime import datetime

        # Return response with tool call metadata
        return ChatResponse(
            response=result.get("response", "I'm sorry, I couldn't process your request."),
            conversation_id=str(conversation_id),
            tool_calls=result.get("tool_calls", []),
            timestamp=datetime.utcnow().isoformat()
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat request: {str(e)}")