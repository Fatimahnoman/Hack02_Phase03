from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from uuid import UUID
from pydantic import BaseModel
from ..core.database import get_session_context
from ..models.task import Task, TaskCreate, TaskUpdate, TaskStatusUpdate
from ..models.user import User
from ..services.auth_service import get_current_user
from ..services.task_service import (
    create_task as service_create_task,
    get_user_tasks as service_get_user_tasks,
    get_task_by_id as service_get_task_by_id,
    update_task as service_update_task,
    delete_task as service_delete_task,
    complete_task as service_complete_task
)

router = APIRouter()

from typing import Optional

from typing import Optional

class TaskResponse(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    status: str
    priority: str
    created_at: str
    updated_at: str
    completed_at: Optional[str] = None

    @classmethod
    def from_task(cls, task):
        return cls(
            id=task.id,
            title=task.title,
            description=task.description or "",
            status=task.status,
            priority=task.priority,
            created_at=task.created_at.isoformat() if task.created_at else "",
            updated_at=task.updated_at.isoformat() if task.updated_at else "",
            completed_at=task.completed_at.isoformat() if task.completed_at else None
        )

@router.post("/tasks", response_model=TaskResponse)
def create_task_endpoint(
    task: TaskCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session_context)
):
    """Create a new task for the current user."""
    created_task = service_create_task(session, task)
    return TaskResponse.from_task(created_task)

@router.get("/tasks", response_model=List[TaskResponse])
def read_tasks(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session_context)
):
    """Get all tasks for the current user."""
    tasks = service_get_user_tasks(session)
    return [TaskResponse.from_task(task) for task in tasks]

@router.get("/tasks/{task_id}", response_model=TaskResponse)
def read_task(
    task_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session_context)
):
    """Get a specific task by ID."""
    task = service_get_task_by_id(session, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskResponse.from_task(task)

@router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task_endpoint(
    task_id: str,
    task: TaskUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session_context)
):
    """Update a specific task."""
    updated_task = service_update_task(session, task_id, task)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskResponse.from_task(updated_task)

@router.delete("/tasks/{task_id}")
def delete_task_endpoint(
    task_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session_context)
):
    """Delete a specific task."""
    success = service_delete_task(session, task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}

@router.patch("/tasks/{task_id}/complete")
def complete_task_endpoint(
    task_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session_context)
):
    """Mark a task as completed."""
    updated_task = service_complete_task(session, task_id)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskResponse.from_task(updated_task)