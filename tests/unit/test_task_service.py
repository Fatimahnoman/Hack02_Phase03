import pytest
from unittest.mock import Mock, MagicMock
from sqlmodel import Session
from datetime import datetime
import uuid
from src.mcp_server.models.task import Task, TaskCreate, TaskUpdate
from src.mcp_server.services.task_service import TaskService


def test_create_task():
    """Test creating a task."""
    # Arrange
    session_mock = Mock(spec=Session)
    task_data = TaskCreate(
        title="Test Task",
        description="This is a test task"
    )

    # Act
    result = TaskService.create_task(session_mock, task_data)

    # Assert - Just verify that the session methods were called
    assert session_mock.add.called
    assert session_mock.commit.called
    assert session_mock.refresh.called


def test_get_task_by_id():
    """Test getting a task by ID."""
    # Arrange
    session_mock = Mock(spec=Session)
    task_id = uuid.uuid4()

    mock_task = Mock(spec=Task)
    session_mock.exec.return_value.first.return_value = mock_task

    # Act
    result = TaskService.get_task_by_id(session_mock, task_id)

    # Assert
    assert result == mock_task
    session_mock.exec.assert_called_once()


def test_get_all_tasks():
    """Test getting all tasks."""
    # Arrange
    session_mock = Mock(spec=Session)

    mock_tasks = [Mock(spec=Task), Mock(spec=Task)]
    session_mock.exec.return_value.all.return_value = mock_tasks

    # Act
    result = TaskService.get_all_tasks(session_mock)

    # Assert
    assert len(result) == 2
    session_mock.exec.assert_called_once()


def test_update_task():
    """Test updating a task."""
    # Arrange
    session_mock = Mock(spec=Session)
    task_id = uuid.uuid4()

    existing_task = Mock(spec=Task)
    existing_task.id = task_id
    existing_task.title = "Old Title"
    existing_task.description = "Old Description"
    existing_task.status = "pending"

    session_mock.exec.return_value.first.return_value = existing_task

    update_data = TaskUpdate(
        title="Updated Title",
        description="Updated Description"
    )

    # Act
    result = TaskService.update_task(session_mock, task_id, update_data)

    # Assert
    assert result == existing_task
    assert existing_task.title == "Updated Title"
    assert existing_task.description == "Updated Description"
    assert session_mock.add.called
    assert session_mock.commit.called
    assert session_mock.refresh.called


def test_delete_task():
    """Test deleting a task."""
    # Arrange
    session_mock = Mock(spec=Session)
    task_id = uuid.uuid4()

    existing_task = Mock(spec=Task)
    existing_task.id = task_id

    session_mock.exec.return_value.first.return_value = existing_task

    # Act
    result = TaskService.delete_task(session_mock, task_id)

    # Assert
    assert result is True
    session_mock.delete.assert_called_once_with(existing_task)
    assert session_mock.commit.called


def test_delete_nonexistent_task():
    """Test deleting a task that doesn't exist."""
    # Arrange
    session_mock = Mock(spec=Session)
    task_id = uuid.uuid4()

    session_mock.exec.return_value.first.return_value = None

    # Act
    result = TaskService.delete_task(session_mock, task_id)

    # Assert
    assert result is False
    session_mock.delete.assert_not_called()


def test_complete_task():
    """Test completing a task."""
    # Arrange
    session_mock = Mock(spec=Session)
    task_id = uuid.uuid4()

    existing_task = Mock(spec=Task)
    existing_task.id = task_id
    existing_task.status = "in-progress"

    session_mock.exec.return_value.first.return_value = existing_task

    # Act
    result = TaskService.complete_task(session_mock, task_id)

    # Assert
    assert result == existing_task
    assert existing_task.status == "completed"
    assert existing_task.completed_at is not None
    assert session_mock.add.called
    assert session_mock.commit.called
    assert session_mock.refresh.called