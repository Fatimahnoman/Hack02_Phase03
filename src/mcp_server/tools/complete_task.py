from mcp.server import Server
from mcp.types import Tool, ArgumentsSchema
from pydantic import BaseModel
from typing import Dict, Any
from sqlmodel import Session
import uuid

from src.mcp_server.models.database import get_session
from src.mcp_server.services.task_service import TaskService
from src.mcp_server.utils.validators import validate_task_id


class CompleteTaskArguments(BaseModel):
    task_id: str


async def complete_task_tool(arguments: CompleteTaskArguments) -> Dict[str, Any]:
    """Mark a task as completed."""
    # Validate task ID
    is_valid, error_msg = validate_task_id(arguments.task_id)
    if not is_valid:
        return {"success": False, "message": error_msg}

    with next(get_session()) as session:
        try:
            completed_task = TaskService.complete_task(session, uuid.UUID(arguments.task_id))
            if not completed_task:
                return {"success": False, "message": f"Task with ID {arguments.task_id} not found"}

            return {
                "success": True,
                "task": {
                    "id": str(completed_task.id),
                    "title": completed_task.title,
                    "description": completed_task.description,
                    "status": completed_task.status,
                    "created_at": completed_task.created_at.isoformat(),
                    "updated_at": completed_task.updated_at.isoformat(),
                    "completed_at": completed_task.completed_at.isoformat() if completed_task.completed_at else None
                },
                "message": "Task marked as completed successfully"
            }
        except Exception as e:
            return {"success": False, "message": f"Failed to complete task: {str(e)}"}