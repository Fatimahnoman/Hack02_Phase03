import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.src.models.task import Task
from backend.src.models.user import User
from sqlmodel import SQLModel, select

# Load environment variables
load_dotenv()

# Get the database URL
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///test.db')
print(f"Connecting to database: {DATABASE_URL}")

# Create engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables if they don't exist
SQLModel.metadata.create_all(bind=engine)

# Create a session
session = SessionLocal()

try:
    # Count total tasks
    total_tasks = session.query(Task).count()
    print(f"Total tasks in database: {total_tasks}")
    
    # Get all tasks with details
    tasks = session.query(Task).all()
    print(f"Found {len(tasks)} tasks:")
    for i, task in enumerate(tasks):
        print(f"  {i+1}. ID: {task.id}, Title: {task.title}, Status: {task.status}, User ID: {task.user_id}")
    
    # Count tasks by user
    from sqlalchemy import func
    user_task_counts = session.query(Task.user_id, func.count(Task.id)).group_by(Task.user_id).all()
    print(f"Tasks by user: {user_task_counts}")
    
    # Get all users
    users = session.query(User).all()
    print(f"Found {len(users)} users:")
    for i, user in enumerate(users):
        print(f"  {i+1}. ID: {user.id}, Email: {user.email}")
        
finally:
    session.close()