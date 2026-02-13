from typing import List, Optional
from sqlmodel import Session, select
from datetime import datetime
from uuid import UUID
from ..models.task import Task, TaskCreate, TaskUpdate, TaskStatusUpdate
from ..models.user import User
import uuid as uuid_lib

def create_task(session: Session, task_data: TaskCreate, user_id: int) -> Task:
    """Create a new task."""
    # Let the model generate its own ID using the default factory
    task = Task(
        title=task_data.title,
        description=task_data.description,
        status=task_data.status,
        priority=task_data.priority,
        user_id=user_id
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

def get_user_tasks(session: Session, user_id: int) -> List[Task]:
    """Get all tasks for a specific user."""
    statement = select(Task).where(Task.user_id == user_id).order_by(Task.created_at.desc())
    return session.exec(statement).all()

def get_task_by_id(session: Session, task_id: str) -> Optional[Task]:
    """Get a task by its ID."""
    statement = select(Task).where(Task.id == task_id)
    return session.exec(statement).first()

def update_task(session: Session, task_id: str, task_update: TaskUpdate) -> Optional[Task]:
    """Update a task with the provided data."""
    task = get_task_by_id(session, task_id)
    if not task:
        return None

    # Update only the fields that are provided
    update_data = task_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)

    # Update the updated_at timestamp
    task.updated_at = datetime.utcnow()

    # Handle completed_at field based on status
    if hasattr(task_update, 'status') and task_update.status == "completed":
        task.completed_at = datetime.utcnow()
    elif hasattr(task_update, 'status') and task_update.status != "completed":
        task.completed_at = None

    session.add(task)
    session.commit()
    session.refresh(task)
    return task

def delete_task(session: Session, task_id: str) -> bool:
    """Delete a task by its ID."""
    task = get_task_by_id(session, task_id)
    if not task:
        return False

    session.delete(task)
    session.commit()
    return True

def complete_task(session: Session, task_id: str) -> Optional[Task]:
    """Mark a task as completed."""
    task = get_task_by_id(session, task_id)
    if not task:
        return None

    task.status = "completed"
    task.completed_at = datetime.utcnow()
    task.updated_at = datetime.utcnow()

    session.add(task)
    session.commit()
    session.refresh(task)
    return task