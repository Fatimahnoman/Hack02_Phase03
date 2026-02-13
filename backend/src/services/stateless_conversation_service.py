"""Stateless conversation service for managing stateless chat interactions using OpenAI agent with MCP tools."""

from typing import Dict, Any, Optional
from datetime import datetime
from .database_service import DatabaseService
from .agent_service import AgentService


class StatelessConversationService:
    """Service to orchestrate the stateless conversation flow using OpenAI agent with MCP tools."""

    def __init__(self, db_service: DatabaseService):
        self.db_service = db_service

    async def process_request(self, user_input: str, user_id: Optional[str], session_metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Process a chat request using OpenAI agent with MCP tools in a stateless manner.

        Args:
            user_input: The user's input message
            user_id: The ID of the user making the request (can be None, will default to valid user)
            session_metadata: Optional metadata about the session

        Returns:
            Dictionary containing the response and related information
        """
        # Ensure we have a valid user_id - if not provided or invalid, use default user
        user_id_int = await self._validate_or_get_default_user_id(user_id)

        # Initialize agent service with validated user_id
        self.agent_service = AgentService(self.db_service.session, user_id=user_id_int)
        # Prepare conversation history (empty for stateless operation)
        conversation_history = []

        try:
            # Process the request through the OpenAI agent with MCP tools
            result = self.agent_service.process_request(
                user_input=user_input,
                conversation_history=conversation_history
            )

            response = result.get("response", "I processed your request.")
            tool_calls = result.get("tool_calls", [])
            status = result.get("status", "success")

            # Prepare tool execution result
            tool_execution_result = {
                "status": status,
                "tool_calls": tool_calls
            } if tool_calls else None

            # Commit the session to ensure all database changes are persisted
            self.db_service.session.commit()

        except Exception as e:
            print(f"Error processing request with agent: {e}")
            # Check if this is an API authentication error
            error_str = str(e).lower()
            if "401" in error_str or "authentication" in error_str or "user not found" in error_str or "invalid api" in error_str:
                response = "I'm sorry, there's an issue with the AI service configuration. Please check that your API key is valid and active."
            else:
                response = "I'm sorry, I encountered an issue processing your request. Please try again."
            tool_execution_result = None
            
            # Rollback the session in case of error
            self.db_service.session.rollback()

        # Get current user state
        try:
            user_state = await self.db_service.get_user_state_summary(str(user_id_int))
        except Exception:
            user_state = {
                "task_count": 0,
                "task_counts_by_status": {},
                "last_activity": datetime.utcnow().isoformat()
            }

        state_reflection = {
            "user_id": str(user_id_int),
            "task_count": user_state.get("task_count", 0),
            "task_counts_by_status": user_state.get("task_counts_by_status", {}),
            "last_updated": user_state.get("last_activity", datetime.utcnow().isoformat()),
        }

        return {
            "response": response,
            "state_reflection": state_reflection,
            "tool_execution_result": tool_execution_result
        }

    async def _validate_or_get_default_user_id(self, user_id: Optional[str]) -> int:
        """
        Validate the provided user_id or get a default valid user_id.
        This ensures we always have a valid user_id to work with.
        """
        # First, try to use the user_id from the request if provided and valid
        if user_id:
            try:
                # Try to convert to int to validate
                user_id_int = int(user_id)

                # Check if the user exists in the database
                from sqlmodel import select
                from ..models.user import User
                existing_user = self.db_service.session.exec(
                    select(User).where(User.id == user_id_int)
                ).first()

                if existing_user:
                    print(f"Using provided user_id: {user_id_int}")  # Debug log
                    return user_id_int
                else:
                    print(f"Provided user_id {user_id_int} does not exist, falling back to default")  # Debug log
            except (ValueError, TypeError) as e:
                print(f"Error converting user_id '{user_id}' to int: {e}")  # Debug log
                # If conversion fails, fall back to default
                pass

        # If no valid user_id provided, try to get the authenticated user from the session
        # This is a fallback to try to get the user from the current session context
        # (though this is tricky in a stateless service)
        
        # If still no user found, look for the first user as a fallback
        from sqlmodel import select
        from ..models.user import User
        from datetime import datetime, timezone

        # Look for any existing user first
        first_user = self.db_service.session.exec(
            select(User).order_by(User.id)
        ).first()

        if first_user:
            print(f"Returning first user as fallback: {first_user.id}")  # Debug log
            return first_user.id
        else:
            # If no users exist, create a default system user
            # This mimics the Phase 5 behavior of having a default user
            from ..services.auth_service import get_password_hash
            import secrets

            # Create a default user with a random secure password
            default_email = "system@example.com"
            default_password = secrets.token_urlsafe(32)  # Random secure password
            hashed_password = get_password_hash(default_password)
            current_time = datetime.now(timezone.utc)

            default_user = User(
                email=default_email,
                hashed_password=hashed_password,
                created_at=current_time,
                updated_at=current_time
            )

            self.db_service.session.add(default_user)
            self.db_service.session.commit()
            self.db_service.session.refresh(default_user)

            print(f"Created and returning new default user: {default_user.id}")  # Debug log
            return default_user.id
