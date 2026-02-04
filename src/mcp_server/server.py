import asyncio
from mcp.server import Server
from mcp.types import Tool, ArgumentsSchema
from pydantic import BaseModel
from typing import Dict, Any
import json
from contextlib import asynccontextmanager
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

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
from src.mcp_server.tools.add_task import add_task_tool
from src.mcp_server.tools.list_tasks import list_tasks_tool
from src.mcp_server.tools.update_task import update_task_tool
from src.mcp_server.tools.complete_task import complete_task_tool
from src.mcp_server.tools.delete_task import delete_task_tool

# Register the tools with the server
server.tool("add_task")(add_task_tool)
server.tool("list_tasks")(list_tasks_tool)
server.tool("update_task")(update_task_tool)
server.tool("complete_task")(complete_task_tool)
server.tool("delete_task")(delete_task_tool)


# Register the server with the context manager
server.lifespan(lifespan)