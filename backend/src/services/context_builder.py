"""
Service layer for building conversation context for AI agents.
"""
import logging
from sqlmodel import Session, select
from typing import List, Optional
from uuid import UUID
from ..models.message import Message, MessageRole
from ..config import settings

import functools
from typing import Dict, Any
import time

logger = logging.getLogger(__name__)

# Simple in-memory cache for conversation contexts
# In production, consider using Redis or similar
_conversation_cache: Dict[UUID, Dict[str, Any]] = {}
_CACHE_TTL_SECONDS = 300  # 5 minutes


class ContextBuilder:
    """
    Service class for building conversation context from database records.
    """

    @staticmethod
    def build_context_from_conversation(session: Session, conversation_id: UUID,
                                     max_tokens: Optional[int] = None) -> List[Message]:
        """
        Build conversation context from database messages for the AI agent.

        Args:
            session: Database session
            conversation_id: ID of the conversation to build context for
            max_tokens: Maximum number of tokens to include (optional)

        Returns:
            List of messages in chronological order forming the conversation context
        """
        logger.info(f"Building context for conversation {conversation_id}")

        # Check if context is in cache
        cached_result = ContextBuilder._get_cached_context(conversation_id)
        if cached_result is not None:
            logger.info(f"Using cached context for conversation {conversation_id}")
            messages = cached_result['messages']
        else:
            # Get all messages for the conversation, ordered by timestamp
            statement = select(Message).where(
                Message.conversation_id == conversation_id
            ).order_by(Message.timestamp)

            messages = session.exec(statement).all()
            logger.info(f"Retrieved {len(messages)} messages for conversation context")

            # Cache the retrieved messages
            ContextBuilder._cache_context(conversation_id, messages)

        # If token limit is specified, implement truncation
        if max_tokens is not None:
            messages = ContextBuilder._truncate_to_token_limit(messages, max_tokens)

        return messages

    @staticmethod
    def _get_cached_context(conversation_id: UUID) -> Optional[Dict[str, Any]]:
        """
        Get cached conversation context if it exists and hasn't expired.

        Args:
            conversation_id: ID of the conversation to check cache for

        Returns:
            Cached context data or None if not found or expired
        """
        if conversation_id in _conversation_cache:
            cached_data = _conversation_cache[conversation_id]
            if time.time() - cached_data['timestamp'] < _CACHE_TTL_SECONDS:
                return cached_data
            else:
                # Remove expired cache entry
                del _conversation_cache[conversation_id]

        return None

    @staticmethod
    def _cache_context(conversation_id: UUID, messages: List[Message]):
        """
        Cache the conversation context.

        Args:
            conversation_id: ID of the conversation
            messages: List of messages to cache
        """
        _conversation_cache[conversation_id] = {
            'messages': messages,
            'timestamp': time.time()
        }
        logger.info(f"Cached context for conversation {conversation_id}")

    @staticmethod
    def invalidate_cache(conversation_id: UUID):
        """
        Invalidate the cache for a specific conversation.

        Args:
            conversation_id: ID of the conversation to invalidate cache for
        """
        if conversation_id in _conversation_cache:
            del _conversation_cache[conversation_id]
            logger.info(f"Invalidated cache for conversation {conversation_id}")

    @staticmethod
    def _truncate_to_token_limit(messages: List[Message], max_tokens: int) -> List[Message]:
        """
        Truncate messages to fit within the token limit, prioritizing recent messages.

        Args:
            messages: List of messages to potentially truncate
            max_tokens: Maximum number of tokens allowed

        Returns:
            List of messages that fit within the token limit
        """
        # This is a simplified token estimation - in practice, you'd use a proper tokenizer
        estimated_tokens = 0
        for message in reversed(messages):  # Start from the end (most recent)
            # Rough estimation: ~4 characters per token
            content_tokens = len(message.content) // 4
            role_tokens = len(str(message.role)) // 4
            estimated_tokens += content_tokens + role_tokens

            if estimated_tokens > max_tokens:
                # Remove this and earlier messages
                cutoff_index = messages.index(message)
                truncated_messages = messages[cutoff_index:]

                logger.info(f"Truncated conversation context from {len(messages)} to {len(truncated_messages)} messages "
                           f"to fit within {max_tokens} token limit")
                return truncated_messages

        return messages

    @staticmethod
    def estimate_token_count(text: str) -> int:
        """
        Estimate the number of tokens in a text string.
        This is a rough approximation - 1 token is roughly 4 characters.

        Args:
            text: Input text to estimate tokens for

        Returns:
            Estimated number of tokens
        """
        if not text:
            return 0
        # Rough estimation: ~4 characters per token
        return len(text) // 4

    @staticmethod
    def validate_token_limit(text: str, max_tokens: int) -> bool:
        """
        Validate that text does not exceed token limit.

        Args:
            text: Text to validate
            max_tokens: Maximum allowed tokens

        Returns:
            True if within limit, False otherwise
        """
        token_count = ContextBuilder.estimate_token_count(text)
        return token_count <= max_tokens

    @staticmethod
    def format_messages_for_agent(messages: List[Message]) -> List[dict]:
        """
        Format messages into a list of dictionaries suitable for AI agent consumption.

        Args:
            messages: List of messages to format

        Returns:
            List of dictionaries with role and content for each message
        """
        formatted_messages = []
        for message in messages:
            role = "user" if message.role == MessageRole.user else "assistant"
            formatted_messages.append({
                "role": role,
                "content": message.content
            })

        return formatted_messages