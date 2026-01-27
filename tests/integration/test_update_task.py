import pytest
from sqlmodel import Session
from uuid import uuid4
from src.mcp_server.models.task import TaskCreate
from src.mcp_server.services.task_service import TaskService
from src.mcp_server.tools.update_task import UpdateTaskArguments, update_task_tool


@pytest.mark.asyncio
async def test_update_task_success(session: Session):
    """Test successful task update."""
    # Arrange - Create a task first
    original_task_data = TaskCreate(title="Original Title", description="Original Description")
    created_task = TaskService.create_task(session, original_task_data)

    arguments = UpdateTaskArguments(
        task_id=str(created_task.id),
        title="Updated Title",
        description="Updated Description",
        status="in-progress"
    )

    # Act
    result = await update_task_tool(arguments)

    # Assert
    assert result["success"] is True
    assert "task" in result
    assert result["task"]["title"] == "Updated Title"
    assert result["task"]["description"] == "Updated Description"
    assert result["task"]["status"] == "in-progress"
    assert result["task"]["id"] == str(created_task.id)
    assert result["message"] == "Task updated successfully"


@pytest.mark.asyncio
async def test_update_task_partial_update(session: Session):
    """Test updating only some fields of a task."""
    # Arrange - Create a task first
    original_task_data = TaskCreate(title="Original Title", description="Original Description", status="pending")
    created_task = TaskService.create_task(session, original_task_data)

    arguments = UpdateTaskArguments(
        task_id=str(created_task.id),
        title="Updated Title"
        # Only updating title, leaving description and status unchanged
    )

    # Act
    result = await update_task_tool(arguments)

    # Assert
    assert result["success"] is True
    assert "task" in result
    assert result["task"]["title"] == "Updated Title"
    # The description should remain the same since it wasn't updated
    assert result["task"]["description"] == "Original Description"
    # The status should remain the same since it wasn't updated
    assert result["task"]["status"] == "pending"
    assert result["message"] == "Task updated successfully"


@pytest.mark.asyncio
async def test_update_task_invalid_id(session: Session):
    """Test updating a task with an invalid ID."""
    # Arrange
    fake_task_id = str(uuid4())

    arguments = UpdateTaskArguments(
        task_id=fake_task_id,
        title="Updated Title"
    )

    # Act
    result = await update_task_tool(arguments)

    # Assert
    assert result["success"] is False
    assert "message" in result
    assert f"not found" in result["message"]


@pytest.mark.asyncio
async def test_update_task_invalid_title(session: Session):
    """Test updating a task with an invalid title."""
    # Arrange - Create a task first
    original_task_data = TaskCreate(title="Original Title", description="Original Description")
    created_task = TaskService.create_task(session, original_task_data)

    arguments = UpdateTaskArguments(
        task_id=str(created_task.id),
        title=""  # Invalid empty title
    )

    # Act
    result = await update_task_tool(arguments)

    # Assert
    assert result["success"] is False
    assert "message" in result
    assert "Title is required" in result["message"]


@pytest.mark.asyncio
async def test_update_task_invalid_status(session: Session):
    """Test updating a task with an invalid status."""
    # Arrange - Create a task first
    original_task_data = TaskCreate(title="Original Title", description="Original Description")
    created_task = TaskService.create_task(session, original_task_data)

    arguments = UpdateTaskArguments(
        task_id=str(created_task.id),
        status="invalid-status"  # Invalid status
    )

    # Act
    result = await update_task_tool(arguments)

    # Assert
    assert result["success"] is False
    assert "message" in result
    assert "Invalid status" in result["message"]