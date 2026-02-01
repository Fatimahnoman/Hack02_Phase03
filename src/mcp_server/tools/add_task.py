from mcp.server import Server
from mcp.types import Tool
from pydantic import BaseModel
from typing import Dict, Any
from sqlmodel import Session
import uuid

from src.mcp_server.models.database import get_session
from src.mcp_server.services.task_service import TaskService
from src.mcp_server.models.task import TaskCreate
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

    # Create task data
    task_data = TaskCreate(
        title=arguments.title,
        description=arguments.description or None
    )

        # Create task in database
    from src.mcp_server.models.database import create_db_and_tables
    create_db_and_tables()  # Ensure tables exist

    with next(get_session()) as session:
        try:
            task = TaskService.create_task(session, task_data)
            return {
                "success": True,
                "task": {
                    "id": str(task.id),
                    "title": task.title,
                    "description": task.description,
                    "status": task.status,
                    "created_at": task.created_at.isoformat(),
                    "updated_at": task.updated_at.isoformat()
                },
                "message": "Task created successfully"
            }
        except Exception as e:
            return {"success": False, "message": f"Failed to create task: {str(e)}"}