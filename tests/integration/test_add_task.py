import pytest
from sqlmodel import Session
from src.mcp_server.models.task import TaskCreate
from src.mcp_server.services.task_service import TaskService
from src.mcp_server.tools.add_task import AddTaskArguments, add_task_tool


@pytest.mark.asyncio
async def test_add_task_success(session: Session):
    """Test successful task creation."""
    # Arrange
    arguments = AddTaskArguments(
        title="Test Task",
        description="This is a test task"
    )

    # Act
    result = await add_task_tool(arguments)

    # Assert
    assert result["success"] is True
    assert "task" in result
    assert result["task"]["title"] == "Test Task"
    assert result["task"]["description"] == "This is a test task"
    assert result["task"]["status"] == "pending"
    assert "id" in result["task"]
    assert result["message"] == "Task created successfully"


@pytest.mark.asyncio
async def test_add_task_without_description(session: Session):
    """Test task creation without description."""
    # Arrange
    arguments = AddTaskArguments(
        title="Test Task",
        description=""
    )

    # Act
    result = await add_task_tool(arguments)

    # Assert
    assert result["success"] is True
    assert "task" in result
    assert result["task"]["title"] == "Test Task"
    assert result["task"]["description"] == "" or result["task"]["description"] is None
    assert result["message"] == "Task created successfully"


@pytest.mark.asyncio
async def test_add_task_invalid_title(session: Session):
    """Test task creation with invalid title."""
    # Arrange
    arguments = AddTaskArguments(
        title="",  # Empty title should fail validation
        description="This is a test task"
    )

    # Act
    result = await add_task_tool(arguments)

    # Assert
    assert result["success"] is False
    assert "message" in result
    assert "Title is required" in result["message"]


@pytest.mark.asyncio
async def test_add_task_long_title(session: Session):
    """Test task creation with overly long title."""
    # Arrange
    long_title = "A" * 300  # This should exceed the 255 character limit
    arguments = AddTaskArguments(
        title=long_title,
        description="This is a test task"
    )

    # Act
    result = await add_task_tool(arguments)

    # Assert
    assert result["success"] is False
    assert "message" in result
    assert "255" in result["message"]  # Should mention the length limit