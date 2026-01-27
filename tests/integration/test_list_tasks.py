import pytest
from sqlmodel import Session
from src.mcp_server.models.task import TaskCreate
from src.mcp_server.services.task_service import TaskService
from src.mcp_server.tools.list_tasks import ListTasksArguments, list_tasks_tool


@pytest.mark.asyncio
async def test_list_tasks_empty(session: Session):
    """Test listing tasks when none exist."""
    # Arrange
    arguments = ListTasksArguments()

    # Act
    result = await list_tasks_tool(arguments)

    # Assert
    assert result["success"] is True
    assert "tasks" in result
    assert result["tasks"] == []
    assert result["total_count"] == 0
    assert result["message"] == "Tasks retrieved successfully"


@pytest.mark.asyncio
async def test_list_tasks_with_data(session: Session):
    """Test listing tasks when tasks exist."""
    # Arrange - Create a task first
    task_data = TaskCreate(title="Test Task", description="Test Description")
    created_task = TaskService.create_task(session, task_data)

    arguments = ListTasksArguments()

    # Act
    result = await list_tasks_tool(arguments)

    # Assert
    assert result["success"] is True
    assert "tasks" in result
    assert len(result["tasks"]) >= 1
    assert result["message"] == "Tasks retrieved successfully"

    # Find our created task in the results
    found_task = None
    for task in result["tasks"]:
        if task["id"] == str(created_task.id):
            found_task = task
            break

    assert found_task is not None
    assert found_task["title"] == "Test Task"
    assert found_task["description"] == "Test Description"


@pytest.mark.asyncio
async def test_list_tasks_with_status_filter(session: Session):
    """Test listing tasks with status filter."""
    # Arrange - Create tasks with different statuses
    task_data1 = TaskCreate(title="Pending Task", description="Test Description", status="pending")
    created_task1 = TaskService.create_task(session, task_data1)

    task_data2 = TaskCreate(title="Completed Task", description="Test Description", status="completed")
    created_task2 = TaskService.create_task(session, task_data2)

    arguments = ListTasksArguments(status_filter="pending")

    # Act
    result = await list_tasks_tool(arguments)

    # Assert
    assert result["success"] is True
    assert "tasks" in result

    # Should only have the pending task
    pending_tasks = [t for t in result["tasks"] if t["id"] == str(created_task1.id)]
    completed_tasks = [t for t in result["tasks"] if t["id"] == str(created_task2.id)]

    assert len(pending_tasks) == 1
    assert len(completed_tasks) == 0
    assert result["message"] == "Tasks retrieved successfully"


@pytest.mark.asyncio
async def test_list_tasks_with_invalid_status(session: Session):
    """Test listing tasks with invalid status filter."""
    # Arrange
    arguments = ListTasksArguments(status_filter="invalid-status")

    # Act
    result = await list_tasks_tool(arguments)

    # Assert
    assert result["success"] is False
    assert "message" in result
    assert "Invalid status" in result["message"]


@pytest.mark.asyncio
async def test_list_tasks_with_pagination(session: Session):
    """Test listing tasks with pagination."""
    # Arrange - Create multiple tasks
    for i in range(5):
        task_data = TaskCreate(title=f"Task {i}", description=f"Description {i}")
        TaskService.create_task(session, task_data)

    arguments = ListTasksArguments(limit=2, offset=0)

    # Act
    result = await list_tasks_tool(arguments)

    # Assert
    assert result["success"] is True
    assert "tasks" in result
    assert len(result["tasks"]) <= 2  # Should respect the limit
    assert result["message"] == "Tasks retrieved successfully"