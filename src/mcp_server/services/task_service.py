from typing import List, Optional
from sqlmodel import Session, select
from src.mcp_server.models.task import Task, TaskCreate, TaskUpdate, TaskStatus
from datetime import datetime
import uuid


class TaskService:
    @staticmethod
    def create_task(session: Session, task_data: TaskCreate) -> Task:
        """Create a new task."""
        task = Task(**task_data.model_dump())
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

    @staticmethod
    def get_task_by_id(session: Session, task_id: uuid.UUID) -> Optional[Task]:
        """Get a task by its ID."""
        statement = select(Task).where(Task.id == task_id)
        return session.exec(statement).first()

    @staticmethod
    def get_all_tasks(
        session: Session,
        status_filter: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Task]:
        """Get all tasks with optional filtering."""
        statement = select(Task)

        if status_filter:
            statement = statement.where(Task.status == status_filter)

        statement = statement.offset(offset).limit(limit).order_by(Task.created_at.desc())
        return session.exec(statement).all()

    @staticmethod
    def update_task(session: Session, task_id: uuid.UUID, task_update: TaskUpdate) -> Optional[Task]:
        """Update a task with the provided data."""
        task = TaskService.get_task_by_id(session, task_id)
        if not task:
            return None

        # Update only the fields that are provided
        update_data = task_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)

        # Update the updated_at timestamp
        task.updated_at = datetime.utcnow()

        # Handle completed_at field based on status
        if value == "completed" and field == "status":
            task.completed_at = datetime.utcnow()
        elif field == "status" and value != "completed":
            task.completed_at = None

        session.add(task)
        session.commit()
        session.refresh(task)
        return task

    @staticmethod
    def delete_task(session: Session, task_id: uuid.UUID) -> bool:
        """Delete a task by its ID."""
        task = TaskService.get_task_by_id(session, task_id)
        if not task:
            return False

        session.delete(task)
        session.commit()
        return True

    @staticmethod
    def complete_task(session: Session, task_id: uuid.UUID) -> Optional[Task]:
        """Mark a task as completed."""
        task = TaskService.get_task_by_id(session, task_id)
        if not task:
            return None

        task.status = "completed"
        task.completed_at = datetime.utcnow()
        task.updated_at = datetime.utcnow()

        session.add(task)
        session.commit()
        session.refresh(task)
        return task