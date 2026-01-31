from typing import Optional, List
from sqlmodel import Session, select
from datetime import datetime
from uuid import UUID
from ..models.conversation import Conversation, ConversationCreate
from ..models.message import Message, MessageCreate


class ConversationService:
    """Service for managing conversations and messages in a stateless agent system."""

    def __init__(self, session: Session):
        self.session = session

    def create_conversation(self, conversation_data: ConversationCreate) -> Conversation:
        """Create a new conversation."""
        conversation = Conversation(
            conversation_metadata=conversation_data.conversation_metadata
        )
        self.session.add(conversation)
        self.session.commit()
        self.session.refresh(conversation)
        return conversation

    def get_conversation(self, conversation_id: UUID) -> Optional[Conversation]:
        """Retrieve a conversation by ID."""
        statement = select(Conversation).where(Conversation.id == conversation_id)
        return self.session.exec(statement).first()

    def get_conversation_history(self, conversation_id: UUID) -> List[Message]:
        """Retrieve all messages in a conversation for agent context."""
        statement = select(Message).where(
            Message.conversation_id == conversation_id,
            Message.role != "tool"  # Exclude tool messages from conversation history
        ).order_by(Message.timestamp)
        return self.session.exec(statement).all()

    def add_message(self, message_data: MessageCreate) -> Message:
        """Add a message to a conversation."""
        message = Message(
            conversation_id=message_data.conversation_id,
            role=message_data.role,
            content=message_data.content,
            tool_call_id=message_data.tool_call_id
        )
        self.session.add(message)
        self.session.commit()
        self.session.refresh(message)
        return message

    def update_conversation(self, conversation_id: UUID, metadata: dict) -> Optional[Conversation]:
        """Update conversation metadata."""
        conversation = self.get_conversation(conversation_id)
        if conversation:
            conversation.conversation_metadata = metadata
            conversation.updated_at = datetime.utcnow()
            self.session.add(conversation)
            self.session.commit()
            self.session.refresh(conversation)
        return conversation