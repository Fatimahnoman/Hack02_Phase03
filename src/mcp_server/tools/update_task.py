from mcp.server import Server
from mcp.types import Tool, ArgumentsSchema
from pydantic import BaseModel
from typing import Dict, Any
from sqlmodel import Session
import uuid

from src.mcp_server.models.database import get_session
from src.mcp_server.services.task_service import TaskService
from src.mcp_server.models.task import TaskUpdate
from src.mcp_server.utils.validators import (
    validate_task_id,
    validate_task_title,
    validate_task_description,
    validate_task_status
)


class UpdateTaskArguments(BaseModel):
    task_id: str
    title: str = None
    description: str = None
    status: str = None


async def update_task_tool(arguments: UpdateTaskArguments) -> Dict[str, Any]:
    """Update a task."""
    # Validate task ID
    is_valid, error_msg = validate_task_id(arguments.task_id)
    if not is_valid:
        return {"success": False, "message": error_msg}

    # Validate other fields if provided
    if arguments.title:
        is_valid, error_msg = validate_task_title(arguments.title)
        if not is_valid:
            return {"success": False, "message": error_msg}

    if arguments.description:
        is_valid, error_msg = validate_task_description(arguments.description)
        if not is_valid:
            return {"success": False, "message": error_msg}

    if arguments.status:
        is_valid, error_msg = validate_task_status(arguments.status)
        if not is_valid:
            return {"success": False, "message": error_msg}

    with next(get_session()) as session:
        try:
            # Prepare update data
            update_data = TaskUpdate(
                title=arguments.title,
                description=arguments.description,
                status=arguments.status
            )

            updated_task = TaskService.update_task(session, uuid.UUID(arguments.task_id), update_data)
            if not updated_task:
                return {"success": False, "message": f"Task with ID {arguments.task_id} not found"}

            return {
                "success": True,
                "task": {
                    "id": str(updated_task.id),
                    "title": updated_task.title,
                    "description": updated_task.description,
                    "status": updated_task.status,
                    "created_at": updated_task.created_at.isoformat(),
                    "updated_at": updated_task.updated_at.isoformat(),
                    "completed_at": updated_task.completed_at.isoformat() if updated_task.completed_at else None
                },
                "message": "Task updated successfully"
            }
        except Exception as e:
            return {"success": False, "message": f"Failed to update task: {str(e)}"}