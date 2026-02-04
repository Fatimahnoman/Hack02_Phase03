from mcp.server import Server
from mcp.types import Tool, ArgumentsSchema
from pydantic import BaseModel
from typing import Dict, Any
from sqlmodel import Session
import uuid

from src.mcp_server.models.database import get_session
from backend.src.core.database import get_session_context  # Use backend's database session
from backend.src.models.todo import TodoCreate, Todo
from backend.src.services.todo_service import create_todo as backend_create_todo
from src.mcp_server.utils.validators import validate_task_title, validate_task_description


class AddTaskArguments(BaseModel):
    title: str
    description: str = ""


async def add_task_tool(arguments: AddTaskArguments) -> Dict[str, Any]:
    """Add a new task."""
    # Validate inputs
    is_valid, error_msg = validate_task_title(arguments.title)
    if not is_valid:
        return {"success": False, "message": error_msg}

    is_valid, error_msg = validate_task_description(arguments.description)
    if not is_valid:
        return {"success": False, "message": error_msg}

    # Create todo data (using backend's Todo model)
    todo_data = TodoCreate(
        title=arguments.title,
        description=arguments.description or None
    )

    # Create todo in database using backend's service
    # We need to simulate a user ID for the todo creation
    # For simplicity, we'll use a default user ID of 1
    # In a real implementation, this should be passed from the context
    user_id = 1  # Default user ID

    try:
        # Get backend session
        backend_session_gen = get_session_context()
        session = next(backend_session_gen)

        try:
            todo = backend_create_todo(session, todo_data, user_id)
            session.commit()  # Commit the transaction

            return {
                "success": True,
                "task": {
                    "id": todo.id,  # Todo ID is integer, not UUID
                    "title": todo.title,
                    "description": todo.description,
                    "completed": todo.completed,
                    "created_at": todo.created_at.isoformat(),
                    "updated_at": todo.updated_at.isoformat()
                },
                "message": "Task created successfully"
            }
        finally:
            session.close()
    except Exception as e:
        return {"success": False, "message": f"Failed to create task: {str(e)}"}