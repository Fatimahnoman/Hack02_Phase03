import os
from dotenv import load_dotenv
from backend.src.core.database import engine
from backend.src.models.task import Task
from backend.src.services.task_service import get_user_tasks
from sqlmodel import Session, select

# Load environment variables
load_dotenv()

def test_task_retrieval():
    # Create a database session
    session = Session(engine)
    
    try:
        # Test retrieving tasks for user ID 1 (the user who owns the tasks)
        user_id = 1
        tasks = get_user_tasks(session, user_id)
        
        print(f"Tasks retrieved for user {user_id}:")
        for i, task in enumerate(tasks):
            print(f"  {i+1}. ID: {task.id}, Title: {task.title}, Status: {task.status}")
        
        print(f"Total tasks for user {user_id}: {len(tasks)}")
        
        # Also try with other user IDs to see if there's a mismatch
        for test_user_id in [2, 10, 20]:  # Try a few other user IDs
            other_tasks = get_user_tasks(session, test_user_id)
            print(f"Tasks for user {test_user_id}: {len(other_tasks)}")
            
    finally:
        session.close()

if __name__ == "__main__":
    test_task_retrieval()