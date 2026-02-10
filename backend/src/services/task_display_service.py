"""
Service to handle the mapping between user-friendly task numbers and internal UUIDs.
"""
from typing import List, Dict, Optional
from sqlmodel import Session, select
from ..models.task import Task


class TaskDisplayService:
    """Service to manage the mapping between display numbers and internal task UUIDs."""

    def __init__(self, session: Session):
        self.session = session

    def get_tasks_with_numbers(self, status: Optional[str] = None, user_id: Optional[int] = None) -> List[Dict]:
        """
        Get all tasks with their display numbers for user presentation.

        Args:
            status: Optional status filter
            user_id: Optional user ID filter

        Returns:
            List of tasks with their display numbers
        """
        statement = select(Task).order_by(Task.created_at.desc())
        if status:
            statement = statement.where(Task.status == status)
        if user_id is not None:
            statement = statement.where(Task.user_id == user_id)

        tasks = self.session.exec(statement).all()

        # Create numbered list for display
        numbered_tasks = []
        for idx, task in enumerate(tasks, 1):
            numbered_tasks.append({
                "display_number": idx,
                "internal_id": str(task.id),
                "title": task.title,
                "description": task.description,
                "status": task.status,
                "priority": task.priority,
                "created_at": task.created_at.isoformat() if task.created_at else None,
                "updated_at": task.updated_at.isoformat() if task.updated_at else None,
                "completed_at": task.completed_at.isoformat() if task.completed_at else None
            })

        return numbered_tasks

    def get_internal_id_from_number(self, display_number: int) -> Optional[str]:
        """
        Convert a display number to an internal task UUID.

        Args:
            display_number: The number shown to the user

        Returns:
            Internal UUID of the task or None if not found
        """
        statement = select(Task).order_by(Task.created_at.desc())
        tasks = self.session.exec(statement).all()

        if 1 <= display_number <= len(tasks):
            return str(tasks[display_number - 1].id)
        return None

    def get_task_by_display_number(self, display_number: int) -> Optional[Task]:
        """
        Get a task by its display number.

        Args:
            display_number: The number shown to the user

        Returns:
            Task object or None if not found
        """
        statement = select(Task).order_by(Task.created_at.desc())
        tasks = self.session.exec(statement).all()

        if 1 <= display_number <= len(tasks):
            return tasks[display_number - 1]
        return None