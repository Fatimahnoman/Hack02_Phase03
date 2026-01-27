from mcp.server import Server
from mcp.types import Tool, ArgumentsSchema
from pydantic import BaseModel
from typing import Dict, Any
from sqlmodel import Session
import uuid

from src.mcp_server.models.database import get_session
from src.mcp_server.services.task_service import TaskService
from src.mcp_server.utils.validators import validate_task_id


class DeleteTaskArguments(BaseModel):
    task_id: str


async def delete_task_tool(arguments: DeleteTaskArguments) -> Dict[str, Any]:
    """Delete a task."""
    # Validate task ID
    is_valid, error_msg = validate_task_id(arguments.task_id)
    if not is_valid:
        return {"success": False, "message": error_msg}

    with next(get_session()) as session:
        try:
            success = TaskService.delete_task(session, uuid.UUID(arguments.task_id))
            if not success:
                return {"success": False, "message": f"Task with ID {arguments.task_id} not found"}

            return {
                "success": True,
                "message": "Task deleted successfully"
            }
        except Exception as e:
            return {"success": False, "message": f"Failed to delete task: {str(e)}"}