import pytest
from datetime import datetime
import uuid
from src.mcp_server.models.task import Task, TaskCreate, TaskUpdate, TaskStatus


def test_task_creation():
    """Test creating a new Task instance."""
    task_data = {
        "title": "Test Task",
        "description": "This is a test task",
        "status": "pending"
    }

    task = Task(**task_data)

    assert task.title == "Test Task"
    assert task.description == "This is a test task"
    assert task.status == "pending"
    assert isinstance(task.id, uuid.UUID)
    assert isinstance(task.created_at, datetime)
    assert isinstance(task.updated_at, datetime)


def test_task_create_schema():
    """Test TaskCreate schema validation."""
    task_create = TaskCreate(
        title="Test Task",
        description="This is a test task"
    )

    assert task_create.title == "Test Task"
    assert task_create.description == "This is a test task"
    assert task_create.status == "pending"  # Default value


def test_task_update_schema():
    """Test TaskUpdate schema."""
    task_update = TaskUpdate(
        title="Updated Task",
        status="completed"
    )

    assert task_update.title == "Updated Task"
    assert task_update.status == "completed"


def test_task_with_optional_fields():
    """Test creating a task with only required fields."""
    task_data = {
        "title": "Minimal Task"
    }

    task = Task(**task_data)

    assert task.title == "Minimal Task"
    assert task.description is None
    assert task.status == "pending"
    assert task.completed_at is None


def test_task_status_enum():
    """Test that task status values are valid."""
    assert TaskStatus.PENDING.value == "pending"
    assert TaskStatus.IN_PROGRESS.value == "in-progress"
    assert TaskStatus.COMPLETED.value == "completed"
    assert TaskStatus.FAILED.value == "failed"