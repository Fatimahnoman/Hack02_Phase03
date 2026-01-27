"""
Service layer for AI agent operations using OpenAI API.
"""
import logging
import os
from typing import List, Optional
from sqlmodel import Session
from uuid import UUID
import openai
from ..models.message import Message, MessageRole
from ..config import settings
from .ai_error_handler import (
    AIServiceError,
    AIServiceAuthenticationError,
    AIServiceRateLimitError,
    AIServiceUnavailableError,
    AIServiceTimeoutError
)
from .circuit_breaker import ai_circuit_breaker, CircuitBreakerError

logger = logging.getLogger(__name__)


class AIAgentService:
    """
    Service class for handling AI agent operations with OpenAI API.
    """

    @staticmethod
    @ai_circuit_breaker
    def generate_response(conversation_history: List[Message], system_prompt: Optional[str] = None) -> str:
        """
        Generate a response from the AI agent based on conversation history.

        Args:
            conversation_history: List of messages in the conversation
            system_prompt: Optional system prompt to guide the AI behavior

        Returns:
            Generated response text from the AI agent
        """
        import time
        start_time = time.time()

        logger.info(f"Generating AI response based on {len(conversation_history)} messages in history")

        try:
            # Format messages for OpenAI API
            formatted_messages = []

            # Add system prompt if provided
            if system_prompt:
                formatted_messages.append({"role": "system", "content": system_prompt})
            else:
                # Default system prompt for context-aware conversation
                formatted_messages.append({
                    "role": "system",
                    "content": "You are a helpful AI assistant. Use the conversation history to provide context-aware responses."
                })

            # Use context builder to format messages properly
            from .context_builder import ContextBuilder
            formatted_context_messages = ContextBuilder.format_messages_for_agent(conversation_history)
            formatted_messages.extend(formatted_context_messages)

            # Determine if using OpenRouter or OpenAI
            api_base_url = os.getenv("OPENAI_API_BASE_URL")
            if api_base_url:
                # Use OpenRouter API
                client = openai.OpenAI(
                    api_key=os.getenv("OPENAI_API_KEY"),
                    base_url=os.getenv("OPENAI_API_BASE_URL")
                )
            else:
                # Use standard OpenAI API
                client = openai.OpenAI(api_key=openai.api_key)

            response = client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                messages=formatted_messages,
                temperature=float(os.getenv("AGENT_TEMPERATURE", "0.7")),
                max_tokens=int(os.getenv("MAX_RESPONSE_TOKENS", "1000")),
            )

            ai_response = response.choices[0].message.content

            if ai_response is None:
                logger.warning("AI response was None, using fallback")
                from ..config import settings
                return settings.fallback_response

            # Calculate and log response time
            response_time = time.time() - start_time
            logger.info(f"AI response generated successfully in {response_time:.2f}s: {ai_response[:50]}...")

            return ai_response

        except openai.AuthenticationError as e:
            logger.error(f"OpenAI API authentication failed: {str(e)}")
            raise AIServiceAuthenticationError(f"AI service authentication error: {str(e)}")

        except openai.RateLimitError as e:
            logger.error(f"OpenAI API rate limit exceeded: {str(e)}")
            raise AIServiceRateLimitError(f"AI service rate limit exceeded: {str(e)}")

        except openai.APIConnectionError as e:
            logger.error(f"Failed to connect to OpenAI API: {str(e)}")
            raise AIServiceUnavailableError(f"AI service connection error: {str(e)}")

        except openai.APITimeoutError as e:
            logger.error(f"OpenAI API request timed out: {str(e)}")
            raise AIServiceTimeoutError(f"AI service timeout error: {str(e)}")

        except Exception as e:
            logger.error(f"Unexpected error generating AI response: {str(e)}")
            raise AIServiceError(f"AI service error: {str(e)}")

    @staticmethod
    def validate_response(response: str) -> bool:
        """
        Validate that the AI response is appropriate before storing.

        Args:
            response: The AI-generated response text

        Returns:
            True if response is valid, False otherwise
        """
        logger.info("Validating AI response")

        if not response or len(response.strip()) == 0:
            logger.warning("AI response is empty")
            return False

        # Check for excessively long responses that might indicate issues
        if len(response) > 10000:  # Arbitrary limit, adjust as needed
            logger.warning(f"AI response is unusually long ({len(response)} chars)")
            return False

        # Additional validation could be added here
        # For example, checking for inappropriate content, etc.

        logger.info("AI response validation passed")
        return True

