"""
Service layer for AI agent operations using OpenRouter API.
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
    Service class for handling AI agent operations with OpenRouter API.
    """

    @staticmethod
    @ai_circuit_breaker
    def generate_response(conversation_history: List[Message], system_prompt: Optional[str] = None) -> str:
        """
        Generate a response from the AI agent based on conversation history using OpenRouter API.

        Args:
            conversation_history: List of messages in the conversation
            system_prompt: Optional system prompt to guide the AI behavior

        Returns:
            Generated response text from the AI agent
        """
        import time
        start_time = time.time()

        logger.info(f"Generating AI response using OpenRouter API based on {len(conversation_history)} messages in history")

        try:
            # Initialize OpenAI client with OpenRouter configuration
            openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
            if not openrouter_api_key:
                logger.error("OPENROUTER_API_KEY environment variable is not set")
                raise AIServiceAuthenticationError("OPENROUTER_API_KEY not configured")

            # Configure OpenAI to use OpenRouter
            openai.api_key = openrouter_api_key
            openai.base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

            # Use context builder to format messages properly
            from .context_builder import ContextBuilder
            formatted_messages = ContextBuilder.format_messages_for_agent(conversation_history)

            # Build messages for OpenAI API (OpenRouter uses OpenAI-compatible format)
            messages = []
            
            # Add system prompt if provided
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            else:
                # Default system message
                messages.append({"role": "system", "content": "You are a helpful AI assistant. Use the conversation history to provide context-aware responses."})

            # Add conversation history
            for msg in formatted_messages:
                role = msg.get("role", "user")
                # Map roles appropriately
                if role == "user":
                    messages.append({"role": "user", "content": msg.get("content", "")})
                elif role == "assistant" or role == "chatbot":
                    messages.append({"role": "assistant", "content": msg.get("content", "")})
                elif role == "system":
                    # Add to system context if needed
                    messages.append({"role": "system", "content": msg.get("content", "")})

            # Call OpenRouter API (using OpenAI-compatible interface)
            response = openai.chat.completions.create(
                model=os.getenv("OPENROUTER_MODEL", "openai/gpt-3.5-turbo"),
                messages=messages,
                temperature=float(os.getenv("AGENT_TEMPERATURE", "0.7")),
                max_tokens=int(os.getenv("MAX_RESPONSE_TOKENS", "1000")),
            )

            # Extract response text from OpenAI response object
            ai_response = response.choices[0].message.content

            if ai_response is None or ai_response.strip() == "":
                logger.warning("AI response was empty, using fallback")
                return settings.fallback_response

            # Calculate and log response time
            response_time = time.time() - start_time
            logger.info(f"AI response generated successfully in {response_time:.2f}s: {ai_response[:50]}...")

            return ai_response

        except openai.AuthenticationError as e:
            logger.error(f"OpenRouter API authentication failed: {str(e)}")
            raise AIServiceAuthenticationError(f"AI service authentication error: {str(e)}")
        
        except openai.RateLimitError as e:
            logger.error(f"OpenRouter API rate limit exceeded: {str(e)}")
            raise AIServiceRateLimitError(f"AI service rate limit exceeded: {str(e)}")
        
        except openai.APIConnectionError as e:
            logger.error(f"Failed to connect to OpenRouter API: {str(e)}")
            raise AIServiceUnavailableError(f"AI service connection error: {str(e)}")
        
        except openai.APITimeoutError as e:
            logger.error(f"OpenRouter API request timed out: {str(e)}")
            raise AIServiceTimeoutError(f"AI service timeout error: {str(e)}")
        
        except openai.APIError as e:
            logger.error(f"OpenRouter API error: {str(e)}")
            raise AIServiceUnavailableError(f"AI service error: {str(e)}")

        except Exception as e:
            error_str = str(e).lower()
            if "connection" in error_str or "timeout" in error_str:
                logger.error(f"Failed to connect to OpenRouter API: {str(e)}")
                raise AIServiceUnavailableError(f"AI service connection error: {str(e)}")
            elif "timeout" in error_str:
                logger.error(f"OpenRouter API request timed out: {str(e)}")
                raise AIServiceTimeoutError(f"AI service timeout error: {str(e)}")
            else:
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

