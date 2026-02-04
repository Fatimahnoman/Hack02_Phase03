from mcp.server import Server
from mcp.types import Tool, ArgumentsSchema
from pydantic import BaseModel
from typing import Dict, Any
from sqlmodel import Session
import uuid

from src.mcp_server.models.database import get_session
from backend.src.core.database import get_session_context  # Use backend's database session
from backend.src.services.todo_service import delete_todo
from src.mcp_server.utils.validators import validate_task_id


class DeleteTaskArguments(BaseModel):
    task_id: str = None
    title: str = None


async def delete_task_tool(arguments: DeleteTaskArguments) -> Dict[str, Any]:
    """Delete a task."""
    # Validate task ID
    is_valid, error_msg = validate_task_id(arguments.task_id)
    if not is_valid:
        return {"success": False, "message": error_msg}

    try:
        # Get backend session
        backend_session_gen = get_session_context()
        session = next(backend_session_gen)

        try:
            # Delete the todo (using default user ID 1)
            user_id = 1  # Default user ID
            success = delete_todo(session, int(arguments.task_id), user_id)

            if not success:
                return {"success": False, "message": f"Task with ID {arguments.task_id} not found"}

            session.commit()  # Commit the transaction

            return {
                "success": True,
                "message": "Task deleted successfully"
            }
        finally:
            session.close()
    except Exception as e:
        return {"success": False, "message": f"Failed to delete task: {str(e)}"}