from mcp.server import Server
from mcp.types import Tool, ArgumentsSchema
from pydantic import BaseModel
from typing import Dict, Any
from sqlmodel import Session

from src.mcp_server.models.database import get_session
from backend.src.core.database import get_session_context  # Use backend's database session
from backend.src.models.todo import Todo
from backend.src.services.todo_service import get_user_todos
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

    try:
        # Get backend session
        backend_session_gen = get_session_context()
        session = next(backend_session_gen)

        try:
            # Get user's todos (using default user ID 1)
            user_id = 1  # Default user ID
            todos = get_user_todos(session, user_id)

            # Apply filters manually since the backend service doesn't support status filtering directly
            filtered_todos = []
            for todo in todos:
                # Map status filter to completed status for todos
                if arguments.status_filter:
                    if arguments.status_filter.lower() == "completed" and not todo.completed:
                        continue
                    elif arguments.status_filter.lower() in ["pending", "in-progress"] and todo.completed:
                        continue

                filtered_todos.append(todo)

            # Apply pagination
            start_idx = arguments.offset
            end_idx = start_idx + arguments.limit
            paginated_todos = filtered_todos[start_idx:end_idx]

            task_list = []
            for todo in paginated_todos:
                task_dict = {
                    "id": todo.id,  # Todo ID is integer
                    "title": todo.title,
                    "description": todo.description,
                    "completed": todo.completed,
                    "created_at": todo.created_at.isoformat(),
                    "updated_at": todo.updated_at.isoformat()
                }
                task_list.append(task_dict)

            total_count = len(filtered_todos)

            return {
                "success": True,
                "tasks": task_list,
                "total_count": total_count,
                "message": "Tasks retrieved successfully"
            }
        finally:
            session.close()
    except Exception as e:
        return {"success": False, "message": f"Failed to retrieve tasks: {str(e)}"}