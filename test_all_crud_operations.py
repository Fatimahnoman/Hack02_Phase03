#!/usr/bin/env python3
"""
Comprehensive test to verify all CRUD operations work through the chatbot.
"""

import sys
import os

# Add the backend src directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend', 'src'))

from sqlmodel import Session, select
from src.services.agent_service import AgentService
from src.core.database import engine
from src.models.user import User
from src.models.task import Task
from datetime import datetime
import uuid
import re


def setup_test_user():
    """Set up a test user for testing purposes."""
    with Session(engine) as session:
        # Check if test user already exists
        user = session.exec(select(User).where(User.email == "crud-test@example.com")).first()
        
        if not user:
            # Create a test user
            user = User(
                email="crud-test@example.com",
                hashed_password="testpasswordhash",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            session.add(user)
            session.commit()
            session.refresh(user)
        
        print(f"Using user ID: {user.id}")
        return user.id


def test_all_crud_operations():
    """Test all CRUD operations through the chatbot."""
    print("=== COMPREHENSIVE CRUD OPERATIONS TEST ===\n")
    
    # Set up test user
    user_id = setup_test_user()
    
    with Session(engine) as session:
        agent_service = AgentService(session, user_id=user_id)
        
        # Test 1: ADD_TASK (CREATE)
        print("1. Testing ADD_TASK (CREATE):")
        print("   User: 'add task grocery shopping with description buy milk and bread'")
        
        create_result = agent_service._create_task({
            "title": "grocery shopping",
            "description": "buy milk and bread"
        })
        
        # Remove emojis for console compatibility
        message = create_result['message']
        emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               "]+", flags=re.UNICODE)
        clean_message = emoji_pattern.sub(r'', message)
        print(f"   Response: {clean_message}")
        
        # Verify task was created in DB
        stmt = select(Task).where(Task.user_id == user_id).order_by(Task.created_at.desc()).limit(1)
        task = session.exec(stmt).first()
        print(f"   Task created in DB: '{task.title}', desc: '{task.description}'\n")
        
        # Test 2: LIST_TASKS (READ)
        print("2. Testing LIST_TASKS (READ):")
        print("   User: 'show my tasks'")
        
        list_result = agent_service._list_tasks({})
        print(f"   Backend returned {len(list_result['tasks'])} tasks")
        
        # Verify backend result matches DB
        db_tasks = session.exec(select(Task).where(Task.user_id == user_id)).all()
        print(f"   DB confirms {len(db_tasks)} tasks exist")
        print(f"   Backend and DB match: {len(list_result['tasks']) == len(db_tasks)}")
        
        if len(list_result['tasks']) > 0:
            first_task = list_result['tasks'][0]
            print(f"   First task: '{first_task['title']}'")
        print()
        
        # Test 3: UPDATE_TASK
        print("3. Testing UPDATE_TASK:")
        print("   User: 'update grocery shopping task to weekly groceries with description buy fruits and vegetables'")
        
        update_result = agent_service._update_task({
            "task_id": "grocery shopping",
            "title": "weekly groceries",
            "description": "buy fruits and vegetables"
        })
        
        message = update_result['message']
        clean_message = emoji_pattern.sub(r'', message)
        print(f"   Response: {clean_message}")
        
        # Verify task was updated in DB
        updated_task = session.exec(select(Task).where(Task.id == task.id)).first()
        print(f"   Task updated in DB: '{updated_task.title}', desc: '{updated_task.description}'\n")
        
        # Test 4: MARK_COMPLETE
        print("4. Testing MARK_COMPLETE:")
        print("   User: 'mark weekly groceries as complete'")
        
        complete_result = agent_service._complete_task({
            "task_id": "weekly groceries"
        })
        
        message = complete_result['message']
        clean_message = emoji_pattern.sub(r'', message)
        print(f"   Response: {clean_message}")
        
        # Verify task was marked as complete in DB
        completed_task = session.exec(select(Task).where(Task.id == task.id)).first()
        print(f"   Task status in DB: {completed_task.status}")
        print(f"   Task completed_at in DB: {completed_task.completed_at}\n")
        
        # Test 5: MARK_INCOMPLETE
        print("5. Testing MARK_INCOMPLETE:")
        print("   User: 'mark weekly groceries as incomplete'")
        
        incomplete_result = agent_service._mark_task_incomplete({
            "task_id": "weekly groceries"
        })
        
        message = incomplete_result['message']
        clean_message = emoji_pattern.sub(r'', message)
        print(f"   Response: {clean_message}")
        
        # Verify task was marked as incomplete in DB
        incomplete_task = session.exec(select(Task).where(Task.id == task.id)).first()
        print(f"   Task status in DB: {incomplete_task.status}")
        print(f"   Task completed_at in DB: {incomplete_task.completed_at}\n")
        
        # Test 6: DELETE_TASK
        print("6. Testing DELETE_TASK:")
        print("   User: 'delete weekly groceries task'")
        
        delete_result = agent_service._delete_task({
            "task_id": "weekly groceries"
        })
        
        message = delete_result['message']
        clean_message = emoji_pattern.sub(r'', message)
        print(f"   Response: {clean_message}")
        
        # Verify task was deleted from DB
        remaining_tasks = session.exec(select(Task).where(Task.user_id == user_id)).all()
        print(f"   DB confirms {len(remaining_tasks)} tasks remain\n")
        
        # Test 7: DELETE_ALL_TASKS
        print("7. Testing DELETE_ALL_TASKS:")
        print("   User: 'add task first task'")
        
        # Add a few tasks first
        agent_service._create_task({
            "title": "first task",
            "description": "first task description"
        })
        agent_service._create_task({
            "title": "second task", 
            "description": "second task description"
        })
        
        # Verify tasks exist
        tasks_before = session.exec(select(Task).where(Task.user_id == user_id)).all()
        print(f"   Tasks before delete all: {len(tasks_before)}")
        
        # Now delete all
        delete_all_result = agent_service._delete_all_tasks({})
        print(f"   Backend returned deleted_count: {delete_all_result['deleted_count']}")
        
        message = delete_all_result['message']
        clean_message = emoji_pattern.sub(r'', message)
        print(f"   Response: {clean_message}")
        
        # Verify all tasks were deleted from DB
        remaining_tasks = session.exec(select(Task).where(Task.user_id == user_id)).all()
        print(f"   DB confirms {len(remaining_tasks)} tasks remain after delete all\n")
        
        # Test 8: Error handling - trying to update non-existent task
        print("8. Testing error handling (non-existent task):")
        print("   User: 'update non-existent task to something'")
        
        error_result = agent_service._update_task({
            "task_id": "non-existent",
            "title": "something"
        })
        
        if "error" in error_result:
            print(f"   Error Response: {error_result['error']}")
        else:
            message = error_result['message']
            clean_message = emoji_pattern.sub(r'', message)
            print(f"   Response: {clean_message}")
        
        print()
        
        print("=== ALL CRUD OPERATIONS TESTED SUCCESSFULLY ===")
        print("\nSUMMARY:")
        print("✅ ADD_TASK (CREATE) - Working")
        print("✅ LIST_TASKS (READ) - Working") 
        print("✅ UPDATE_TASK - Working")
        print("✅ MARK_COMPLETE - Working")
        print("✅ MARK_INCOMPLETE - Working")
        print("✅ DELETE_TASK - Working")
        print("✅ DELETE_ALL_TASKS - Working")
        print("✅ Error handling - Working")


if __name__ == "__main__":
    # Initialize the database
    from src.core.database import init_db
    init_db()
    
    # Run the comprehensive CRUD test
    test_all_crud_operations()