from mcp.server import Server
from mcp.types import Tool, ArgumentsSchema
from pydantic import BaseModel
from typing import Dict, Any
from sqlmodel import Session
import uuid

from src.mcp_server.models.database import get_session
from backend.src.core.database import get_session_context  # Use backend's database session
from backend.src.models.todo import TodoUpdate
from backend.src.services.todo_service import update_todo
from src.mcp_server.utils.validators import (
    validate_task_id,
    validate_task_title,
    validate_task_description,
    validate_task_status
)


class UpdateTaskArguments(BaseModel):
    task_id: str = None
    title: str = None
    description: str = None
    status: str = None


async def update_task_tool(arguments: UpdateTaskArguments) -> Dict[str, Any]:
    """Update a task."""
    # Validate task ID
    if arguments.task_id:
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

    try:
        # Convert arguments to backend TodoUpdate format
        # Map status to completed flag for todos
        completed = None
        if arguments.status:
            if arguments.status.lower() == "completed":
                completed = True
            elif arguments.status.lower() in ["pending", "in-progress"]:
                completed = False

        # Prepare update data
        update_data = TodoUpdate(
            title=arguments.title,
            description=arguments.description,
            completed=completed,  # Use completed flag for todos
            due_date=None  # Don't update due date
        )

        # Get backend session
        backend_session_gen = get_session_context()
        session = next(backend_session_gen)

        try:
            # Update the todo (using default user ID 1)
            user_id = 1  # Default user ID
            updated_todo = update_todo(session, int(arguments.task_id), update_data, user_id)

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
                "message": "Task updated successfully"
            }
        finally:
            session.close()
    except Exception as e:
        return {"success": False, "message": f"Failed to update task: {str(e)}"}