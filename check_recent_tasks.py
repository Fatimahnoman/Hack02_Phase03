import os
from dotenv import load_dotenv
from backend.src.core.database import engine
from backend.src.models.task import Task
from backend.src.services.task_service import get_user_tasks
from sqlmodel import Session, select

# Load environment variables
load_dotenv()

def check_latest_tasks():
    # Create a database session
    session = Session(engine)
    
    try:
        # Get all tasks ordered by creation date (most recent first)
        statement = select(Task).order_by(Task.created_at.desc()).limit(5)
        recent_tasks = session.exec(statement).all()
        
        print("5 most recent tasks in the database:")
        for i, task in enumerate(recent_tasks):
            print(f"  {i+1}. ID: {task.id}, Title: {task.title}, Status: {task.status}, User ID: {task.user_id}, Created: {task.created_at}")
        
        # Specifically look for the 'grocerry' task
        grocerry_statement = select(Task).where(Task.title.contains('grocerry')).order_by(Task.created_at.desc())
        grocerry_tasks = session.exec(grocerry_statement).all()
        
        print(f"\nTasks with 'grocerry' in the title: {len(grocerry_tasks)}")
        for i, task in enumerate(grocerry_tasks):
            print(f"  {i+1}. ID: {task.id}, Title: {task.title}, Description: {task.description}, User ID: {task.user_id}, Created: {task.created_at}")
        
    finally:
        session.close()

if __name__ == "__main__":
    check_latest_tasks()