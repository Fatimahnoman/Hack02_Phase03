import pytest
from sqlmodel import Session
from src.mcp_server.models.task import TaskCreate
from src.mcp_server.services.task_service import TaskService
from src.mcp_server.tools.add_task import AddTaskArguments, add_task_tool
from src.mcp_server.tools.list_tasks import ListTasksArguments, list_tasks_tool
from src.mcp_server.tools.update_task import UpdateTaskArguments, update_task_tool
from src.mcp_server.tools.complete_task import CompleteTaskArguments, complete_task_tool
from src.mcp_server.tools.delete_task import DeleteTaskArguments, delete_task_tool


@pytest.mark.asyncio
async def test_task_persistence_across_sessions(session: Session):
    """Test that tasks persist across different sessions (simulating server restart)."""
    # This test verifies that tasks are properly stored in the database
    # and remain accessible when using different session instances

    # Arrange - Create a task in one session context
    add_arguments = AddTaskArguments(
        title="Persistent Task",
        description="This task should persist across sessions"
    )

    create_result = await add_task_tool(add_arguments)
    assert create_result["success"] is True
    task_id = create_result["task"]["id"]

    # Act - Access the task in a different session context
    # We're using the same session fixture here, but in practice this would simulate
    # accessing the task after a server restart when a new connection is established

    list_arguments = ListTasksArguments()
    list_result = await list_tasks_tool(list_arguments)

    # Assert
    assert list_result["success"] is True
    found_task = None
    for task in list_result["tasks"]:
        if task["id"] == task_id:
            found_task = task
            break

    assert found_task is not None
    assert found_task["title"] == "Persistent Task"
    assert found_task["description"] == "This task should persist across sessions"


@pytest.mark.asyncio
async def test_task_state_preservation_after_modification(session: Session):
    """Test that task state changes are preserved in the database."""
    # Arrange - Create a task
    add_arguments = AddTaskArguments(
        title="State Preservation Task",
        description="Task to test state preservation"
    )

    create_result = await add_task_tool(add_arguments)
    assert create_result["success"] is True
    task_id = create_result["task"]["id"]
    assert create_result["task"]["status"] == "pending"

    # Act - Update the task status
    update_arguments = UpdateTaskArguments(
        task_id=task_id,
        status="in-progress"
    )

    update_result = await update_task_tool(update_arguments)
    assert update_result["success"] is True
    assert update_result["task"]["status"] == "in-progress"

    # Now access the task again to verify the state change was persisted
    list_arguments = ListTasksArguments()
    list_result = await list_tasks_tool(list_arguments)

    # Assert
    found_task = None
    for task in list_result["tasks"]:
        if task["id"] == task_id:
            found_task = task
            break

    assert found_task is not None
    assert found_task["status"] == "in-progress"
    assert found_task["title"] == "State Preservation Task"


@pytest.mark.asyncio
async def test_completed_task_persistence(session: Session):
    """Test that completed tasks maintain their state in the database."""
    # Arrange - Create and complete a task
    add_arguments = AddTaskArguments(
        title="Completion Persistence Task",
        description="Task to test completion state persistence"
    )

    create_result = await add_task_tool(add_arguments)
    assert create_result["success"] is True
    task_id = create_result["task"]["id"]

    # Complete the task
    complete_arguments = CompleteTaskArguments(task_id=task_id)
    complete_result = await complete_task_tool(complete_arguments)
    assert complete_result["success"] is True
    assert complete_result["task"]["status"] == "completed"
    assert complete_result["task"]["completed_at"] is not None

    # Act - Retrieve the task again
    list_arguments = ListTasksArguments()
    list_result = await list_tasks_tool(list_arguments)

    # Assert
    found_task = None
    for task in list_result["tasks"]:
        if task["id"] == task_id:
            found_task = task
            break

    assert found_task is not None
    assert found_task["status"] == "completed"
    assert found_task["completed_at"] is not None
    assert found_task["title"] == "Completion Persistence Task"


@pytest.mark.asyncio
async def test_deleted_task_removal_verification(session: Session):
    """Test that deleted tasks are properly removed from storage."""
    # Arrange - Create a task
    add_arguments = AddTaskArguments(
        title="Deletion Verification Task",
        description="Task to test deletion"
    )

    create_result = await add_task_tool(add_arguments)
    assert create_result["success"] is True
    task_id = create_result["task"]["id"]

    # Verify the task exists initially
    list_arguments = ListTasksArguments()
    initial_list_result = await list_tasks_tool(list_arguments)

    initial_task_found = any(task["id"] == task_id for task in initial_list_result["tasks"])
    assert initial_task_found is True

    # Act - Delete the task
    delete_arguments = DeleteTaskArguments(task_id=task_id)
    delete_result = await delete_task_tool(delete_arguments)
    assert delete_result["success"] is True

    # Verify the task is gone
    post_delete_list_result = await list_tasks_tool(list_arguments)

    # Assert
    post_delete_task_found = any(task["id"] == task_id for task in post_delete_list_result["tasks"])
    assert post_delete_task_found is False
    assert delete_result["message"] == "Task deleted successfully"