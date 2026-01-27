import pytest
from sqlmodel import Session
from uuid import uuid4
from src.mcp_server.models.task import TaskCreate
from src.mcp_server.services.task_service import TaskService
from src.mcp_server.tools.complete_task import CompleteTaskArguments, complete_task_tool


@pytest.mark.asyncio
async def test_complete_task_success(session: Session):
    """Test successfully completing a task."""
    # Arrange - Create a task first
    original_task_data = TaskCreate(title="Task to Complete", description="Original Description", status="in-progress")
    created_task = TaskService.create_task(session, original_task_data)

    arguments = CompleteTaskArguments(
        task_id=str(created_task.id)
    )

    # Act
    result = await complete_task_tool(arguments)

    # Assert
    assert result["success"] is True
    assert "task" in result
    assert result["task"]["title"] == "Task to Complete"
    assert result["task"]["status"] == "completed"
    assert result["task"]["id"] == str(created_task.id)
    assert result["task"]["completed_at"] is not None
    assert result["message"] == "Task marked as completed successfully"


@pytest.mark.asyncio
async def test_complete_task_invalid_id(session: Session):
    """Test completing a task with an invalid ID."""
    # Arrange
    fake_task_id = str(uuid4())

    arguments = CompleteTaskArguments(
        task_id=fake_task_id
    )

    # Act
    result = await complete_task_tool(arguments)

    # Assert
    assert result["success"] is False
    assert "message" in result
    assert f"not found" in result["message"]


@pytest.mark.asyncio
async def test_complete_task_already_completed(session: Session):
    """Test completing a task that's already completed."""
    # Arrange - Create and complete a task first
    original_task_data = TaskCreate(title="Already Completed Task", description="Original Description", status="completed")
    created_task = TaskService.create_task(session, original_task_data)

    # Manually set as completed
    completed_task = TaskService.complete_task(session, created_task.id)

    arguments = CompleteTaskArguments(
        task_id=str(completed_task.id)
    )

    # Act
    result = await complete_task_tool(arguments)

    # Assert - Should still succeed since completing a completed task is idempotent
    assert result["success"] is True
    assert "task" in result
    assert result["task"]["status"] == "completed"
    assert result["message"] == "Task marked as completed successfully"


@pytest.mark.asyncio
async def test_complete_task_invalid_uuid_format(session: Session):
    """Test completing a task with an invalid UUID format."""
    # Arrange
    arguments = CompleteTaskArguments(
        task_id="invalid-uuid-format"
    )

    # Act
    result = await complete_task_tool(arguments)

    # Assert
    assert result["success"] is False
    assert "message" in result
    assert "Invalid task ID format" in result["message"]