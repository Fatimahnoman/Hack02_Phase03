from mcp.server import Server
from mcp.types import Tool
from pydantic import BaseModel
from typing import Dict, Any
from sqlmodel import Session

from src.mcp_server.models.database import get_session
from src.mcp_server.services.task_service import TaskService
from src.mcp_server.utils.validators import validate_task_status, validate_pagination_params


class ListTasksArguments(BaseModel):
    status_filter: str = None
    limit: int = 100
    offset: int = 0


async def list_tasks_tool(arguments: ListTasksArguments) -> Dict[str, Any]:
    """List all tasks with optional filtering."""
    # Validate pagination params
    is_valid, error_msg = validate_pagination_params(arguments.limit, arguments.offset)
    if not is_valid:
        return {"success": False, "message": error_msg}

    # Validate status filter if provided
    if arguments.status_filter:
        is_valid, error_msg = validate_task_status(arguments.status_filter)
        if not is_valid:
            return {"success": False, "message": error_msg}

    from src.mcp_server.models.database import create_db_and_tables
    create_db_and_tables()  # Ensure tables exist

    with next(get_session()) as session:
        try:
            tasks = TaskService.get_all_tasks(
                session,
                status_filter=arguments.status_filter,
                limit=arguments.limit,
                offset=arguments.offset
            )

            task_list = []
            for task in tasks:
                task_dict = {
                    "id": str(task.id),
                    "title": task.title,
                    "description": task.description,
                    "status": task.status,
                    "created_at": task.created_at.isoformat(),
                    "updated_at": task.updated_at.isoformat(),
                    "completed_at": task.completed_at.isoformat() if task.completed_at else None
                }
                task_list.append(task_dict)

            # In a real implementation, we'd want to get the total count from a separate query
            # For now, we'll just return the length of the current result
            total_count = len(task_list)

            return {
                "success": True,
                "tasks": task_list,
                "total_count": total_count,
                "message": "Tasks retrieved successfully"
            }
        except Exception as e:
            return {"success": False, "message": f"Failed to retrieve tasks: {str(e)}"}