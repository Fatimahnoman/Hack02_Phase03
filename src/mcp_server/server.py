import asyncio
from mcp.server import Server
from mcp.types import Tool
from pydantic import BaseModel
from typing import Dict, Any
import json
from contextlib import asynccontextmanager

from config.settings import settings
from src.mcp_server.models.database import get_session, create_db_and_tables
from src.mcp_server.services.task_service import TaskService
from src.mcp_server.models.task import TaskCreate, TaskUpdate
from src.mcp_server.utils.validators import (
    validate_task_title,
    validate_task_description,
    validate_task_status,
    validate_task_id,
    validate_pagination_params
)


# Global server instance
server = Server("mcp-task-manager")


@asynccontextmanager
async def lifespan():
    """Lifespan context manager for the server."""
    # Startup
    create_db_and_tables()
    yield
    # Shutdown
    # Any cleanup can go here


# Tool schemas
class AddTaskArguments(BaseModel):
    title: str
    description: str = ""


class ListTasksArguments(BaseModel):
    status_filter: str = None
    limit: int = 100
    offset: int = 0


class UpdateTaskArguments(BaseModel):
    task_id: str
    title: str = None
    description: str = None
    status: str = None


class CompleteTaskArguments(BaseModel):
    task_id: str


class DeleteTaskArguments(BaseModel):
    task_id: str


# Import the individual tools
from src.mcp_server.tools.add_task import add_task_tool, AddTaskArguments
from src.mcp_server.tools.list_tasks import list_tasks_tool, ListTasksArguments
from src.mcp_server.tools.update_task import update_task_tool, UpdateTaskArguments
from src.mcp_server.tools.complete_task import complete_task_tool, CompleteTaskArguments
from src.mcp_server.tools.delete_task import delete_task_tool, DeleteTaskArguments

# Register the tools with the server using the call_tool decorator
# The tool name will be inferred from the function name
@server.call_tool()
def add_task(arguments: AddTaskArguments):
    return add_task_tool(arguments)

@server.call_tool()
def list_tasks(arguments: ListTasksArguments):
    return list_tasks_tool(arguments)

@server.call_tool()
def update_task(arguments: UpdateTaskArguments):
    return update_task_tool(arguments)

@server.call_tool()
def complete_task(arguments: CompleteTaskArguments):
    return complete_task_tool(arguments)

@server.call_tool()
def delete_task(arguments: DeleteTaskArguments):
    return delete_task_tool(arguments)

# Register the server with the context manager
server.lifespan(lifespan)