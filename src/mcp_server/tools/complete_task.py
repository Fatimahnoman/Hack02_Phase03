from mcp.server import Server
from mcp.types import Tool, ArgumentsSchema
from pydantic import BaseModel
from typing import Dict, Any
from sqlmodel import Session
import uuid

from src.mcp_server.models.database import get_session
from backend.src.core.database import get_session_context  # Use backend's database session
from backend.src.services.todo_service import toggle_todo_completion
from src.mcp_server.utils.validators import validate_task_id


class CompleteTaskArguments(BaseModel):
    task_id: str = None
    title: str = None


async def complete_task_tool(arguments: CompleteTaskArguments) -> Dict[str, Any]:
    """Mark a task as completed."""
    # Validate task ID
    is_valid, error_msg = validate_task_id(arguments.task_id)
    if not is_valid:
        return {"success": False, "message": error_msg}

    try:
        # Get backend session
        backend_session_gen = get_session_context()
        session = next(backend_session_gen)

        try:
            # Complete the todo (using default user ID 1)
            user_id = 1  # Default user ID
            updated_todo = toggle_todo_completion(session, int(arguments.task_id), True, user_id)

            if not updated_todo:
                return {"success": False, "message": f"Task with ID {arguments.task_id} not found"}

            session.commit()  # Commit the transaction

            return {
                "success": True,
                "task": {
                    "id": updated_todo.id,  # Todo ID is integer
                    "title": updated_todo.title,
                    "description": updated_todo.description,
                    "completed": updated_todo.completed,
                    "created_at": updated_todo.created_at.isoformat(),
                    "updated_at": updated_todo.updated_at.isoformat()
                },
                "message": "Task marked as completed successfully"
            }
        finally:
            session.close()
    except Exception as e:
        return {"success": False, "message": f"Failed to complete task: {str(e)}"}