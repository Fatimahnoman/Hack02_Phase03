from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlmodel import Session
from typing import List
from pydantic import BaseModel
from ..database.database import get_session
from ..models.todo import Todo, TodoCreate, TodoRead, TodoUpdate
from ..models.user import User
from ..services.auth_service import get_current_user
from ..services.todo_service import (
    get_user_todos,
    get_todo_by_id,
    create_todo,
    update_todo,
    delete_todo,
    toggle_todo_completion
)

router = APIRouter()

class TodoStatusUpdate(BaseModel):
    completed: bool

@router.post("/", response_model=TodoRead)
def create_todo_endpoint(
    todo: TodoCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    # Create a new todo associated with the current user
    return create_todo(session, todo, current_user.id)

@router.get("/", response_model=List[TodoRead])
def read_todos(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    # Get all todos for the current user
    return get_user_todos(session, current_user.id)

@router.get("/{todo_id}", response_model=TodoRead)
def read_todo(
    todo_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    # Get a specific todo for the current user
    todo = get_todo_by_id(session, todo_id, current_user.id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@router.put("/{todo_id}", response_model=TodoRead)
def update_todo_endpoint(
    todo_id: int,
    todo: TodoUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    # Update a specific todo for the current user
    updated_todo = update_todo(session, todo_id, todo, current_user.id)
    if not updated_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return updated_todo

@router.delete("/{todo_id}")
def delete_todo_endpoint(
    todo_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    # Delete a specific todo for the current user
    success = delete_todo(session, todo_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"message": "Todo deleted successfully"}

@router.patch("/{todo_id}/status")
def update_todo_status(
    todo_id: int,
    status_update: TodoStatusUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    # Update the completion status of a specific todo
    updated_todo = toggle_todo_completion(session, todo_id, status_update.completed, current_user.id)
    if not updated_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"id": updated_todo.id, "completed": updated_todo.completed}