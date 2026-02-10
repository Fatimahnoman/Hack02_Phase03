"""Database service for handling all database operations."""

from typing import List, Optional, Dict, Any
from sqlmodel import Session, select
from datetime import datetime
from ..models.user import User, UserCreate
from ..models.task import Task, TaskCreate, TaskUpdate


class DatabaseService:
    """Service class to handle all database operations."""

    def __init__(self, session: Session):
        self.session = session

    # User operations
    async def create_user(self, user_create: UserCreate) -> User:
        """Create a new user in the database."""
        user = User.from_orm(user_create) if hasattr(User, 'from_orm') else User(**user_create.dict())
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    async def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Retrieve a user by their ID from the database."""
        try:
            user_id_int = int(user_id)
        except (ValueError, TypeError):
            # If user_id is not a valid integer, return None
            return None
            
        statement = select(User).where(User.id == user_id_int)
        result = self.session.exec(statement)
        return result.first()

    # Task operations
    async def get_user_tasks(self, user_id: str, status_filter: Optional[str] = None) -> List[Task]:
        """Retrieve all tasks for a specific user, optionally filtered by status."""
        try:
            user_id_int = int(user_id)
        except (ValueError, TypeError):
            # If user_id is not a valid integer, return empty list
            return []
            
        statement = select(Task).where(Task.user_id == user_id_int)

        if status_filter:
            statement = statement.where(Task.status == status_filter)

        statement = statement.order_by(Task.created_at.desc())
        result = self.session.exec(statement)
        return result.all()

    async def create_task(self, task_create: TaskCreate) -> Task:
        """Create a new task in the database."""
        task = Task.from_orm(task_create) if hasattr(Task, 'from_orm') else Task(**task_create.dict())
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    async def update_task(self, task_id: str, task_update: TaskUpdate) -> Optional[Task]:
        """Update an existing task in the database."""
        statement = select(Task).where(Task.id == task_id)
        result = self.session.exec(statement)
        task = result.first()

        if not task:
            return None

        update_data = task_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)

        task.updated_at = datetime.utcnow()

        if hasattr(task_update, 'status') and task_update.status and task_update.status == 'completed':
            task.completed_at = datetime.utcnow()

        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    async def delete_task(self, task_id: str) -> bool:
        """Delete a task from the database."""
        statement = select(Task).where(Task.id == task_id)
        result = self.session.exec(statement)
        task = result.first()

        if not task:
            return False

        self.session.delete(task)
        self.session.commit()
        return True

    # Utility operations
    async def get_user_state_summary(self, user_id: str) -> Dict[str, Any]:
        """Get a summary of user state."""
        try:
            user_id_int = int(user_id)
        except (ValueError, TypeError):
            # If user_id is not a valid integer, return empty summary
            return {}

        user = await self.get_user_by_id(user_id_int)
        if not user:
            # If user doesn't exist, return empty summary but don't error
            return {
                "user_id": user_id_int,
                "task_count": 0,
                "task_counts_by_status": {},
                "last_activity": datetime.utcnow().isoformat()
            }

        # Get task counts by status
        all_tasks = await self.get_user_tasks(user_id_int)
        task_counts = {}
        for task in all_tasks:
            status = task.status
            task_counts[status] = task_counts.get(status, 0) + 1

        return {
            "user_id": user_id_int,
            "task_count": len(all_tasks),
            "task_counts_by_status": task_counts,
            "last_activity": datetime.utcnow().isoformat()
        }
