from sqlmodel import Session, select
from typing import List, Optional
from ..models.todo import Todo, TodoCreate, TodoUpdate, TodoRead
from ..models.user import User

def get_user_todos(session: Session, user_id: int) -> List[Todo]:
    """Get all todos for a specific user"""
    statement = select(Todo).where(Todo.user_id == user_id)
    todos = session.exec(statement).all()
    return todos

def get_todo_by_id(session: Session, todo_id: int, user_id: int) -> Optional[Todo]:
    """Get a specific todo by ID for a specific user"""
    statement = select(Todo).where(Todo.id == todo_id, Todo.user_id == user_id)
    todo = session.exec(statement).first()
    return todo

def create_todo(session: Session, todo: TodoCreate, user_id: int) -> Todo:
    """Create a new todo for a user"""
    db_todo = Todo(
        title=todo.title,
        description=todo.description,
        due_date=todo.due_date,
        completed=False,  # Default to not completed
        user_id=user_id
    )
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo

def update_todo(session: Session, todo_id: int, todo_update: TodoUpdate, user_id: int) -> Optional[Todo]:
    """Update a specific todo for a user"""
    db_todo = get_todo_by_id(session, todo_id, user_id)
    if not db_todo:
        return None

    # Update the todo with new values
    todo_data = todo_update.model_dump(exclude_unset=True)
    for key, value in todo_data.items():
        setattr(db_todo, key, value)

    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo

def delete_todo(session: Session, todo_id: int, user_id: int) -> bool:
    """Delete a specific todo for a user"""
    db_todo = get_todo_by_id(session, todo_id, user_id)
    if not db_todo:
        return False

    session.delete(db_todo)
    session.commit()
    return True

def toggle_todo_completion(session: Session, todo_id: int, completed: bool, user_id: int) -> Optional[Todo]:
    """Toggle the completion status of a specific todo for a user"""
    db_todo = get_todo_by_id(session, todo_id, user_id)
    if not db_todo:
        return None

    db_todo.completed = completed
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo