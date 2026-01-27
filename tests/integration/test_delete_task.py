import pytest
from sqlmodel import Session
from uuid import uuid4
from src.mcp_server.models.task import TaskCreate
from src.mcp_server.services.task_service import TaskService
from src.mcp_server.tools.delete_task import DeleteTaskArguments, delete_task_tool


@pytest.mark.asyncio
async def test_delete_task_success(session: Session):
    """Test successfully deleting a task."""
    # Arrange - Create a task first
    original_task_data = TaskCreate(title="Task to Delete", description="Description to be deleted")
    created_task = TaskService.create_task(session, original_task_data)

    arguments = DeleteTaskArguments(
        task_id=str(created_task.id)
    )

    # Act
    result = await delete_task_tool(arguments)

    # Assert
    assert result["success"] is True
    assert result["message"] == "Task deleted successfully"

    # Verify the task was actually deleted
    remaining_task = TaskService.get_task_by_id(session, created_task.id)
    assert remaining_task is None


@pytest.mark.asyncio
async def test_delete_task_invalid_id(session: Session):
    """Test deleting a task with an invalid ID."""
    # Arrange
    fake_task_id = str(uuid4())

    arguments = DeleteTaskArguments(
        task_id=fake_task_id
    )

    # Act
    result = await delete_task_tool(arguments)

    # Assert
    assert result["success"] is False
    assert "message" in result
    assert f"not found" in result["message"]


@pytest.mark.asyncio
async def test_delete_task_twice(session: Session):
    """Test deleting the same task twice."""
    # Arrange - Create a task first
    original_task_data = TaskCreate(title="Task to Delete Twice", description="Description")
    created_task = TaskService.create_task(session, original_task_data)

    # Delete the task once
    arguments = DeleteTaskArguments(
        task_id=str(created_task.id)
    )

    # Act - First deletion
    result1 = await delete_task_tool(arguments)

    # Assert - First deletion should succeed
    assert result1["success"] is True
    assert result1["message"] == "Task deleted successfully"

    # Act - Second deletion attempt
    result2 = await delete_task_tool(arguments)

    # Assert - Second deletion should fail
    assert result2["success"] is False
    assert "message" in result2
    assert f"not found" in result2["message"]


@pytest.mark.asyncio
async def test_delete_task_invalid_uuid_format(session: Session):
    """Test deleting a task with an invalid UUID format."""
    # Arrange
    arguments = DeleteTaskArguments(
        task_id="invalid-uuid-format"
    )

    # Act
    result = await delete_task_tool(arguments)

    # Assert
    assert result["success"] is False
    assert "message" in result
    assert "Invalid task ID format" in result["message"]