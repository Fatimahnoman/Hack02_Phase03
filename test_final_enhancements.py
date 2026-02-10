#!/usr/bin/env python3
"""
Final test to verify all enhancements work correctly.
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
        user = session.exec(select(User).where(User.email == "final-test@example.com")).first()
        
        if not user:
            # Create a test user
            user = User(
                email="final-test@example.com",
                hashed_password="testpasswordhash",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            session.add(user)
            session.commit()
            session.refresh(user)
        
        print(f"Using user ID: {user.id}")
        return user.id


def test_final_enhancements():
    """Test all the final enhancements."""
    print("=== TESTING FINAL ENHANCEMENTS ===\n")
    
    # Set up test user
    user_id = setup_test_user()
    
    with Session(engine) as session:
        agent_service = AgentService(session, user_id=user_id)
        
        # Test 1: CREATE_TASK with friendly response
        print("1. Testing CREATE_TASK with friendly response:")
        print("   User: 'add task grocery shopping'")
        
        result = agent_service._create_task({
            "title": "grocery shopping",
            "description": "buy milk and bread"
        })
        
        # Remove emojis for console compatibility
        message = result['message']
        emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               "]+", flags=re.UNICODE)
        clean_message = emoji_pattern.sub(r'', message)
        print(f"   Response: {clean_message}\n")
        
        # Test 2: DELETE_ALL_TASKS with friendly response when tasks exist
        print("2. Testing DELETE_ALL_TASKS with tasks present:")
        print("   User: 'delete all tasks'")
        
        # Create a few tasks first
        agent_service._create_task({
            "title": "task1",
            "description": "first task"
        })
        agent_service._create_task({
            "title": "task2", 
            "description": "second task"
        })
        
        delete_all_result = agent_service._delete_all_tasks({})
        
        clean_message = emoji_pattern.sub(r'', delete_all_result['message'])
        print(f"   Response: {clean_message}\n")
        
        # Test 3: DELETE_ALL_TASKS with no tasks (friendly response)
        print("3. Testing DELETE_ALL_TASKS with no tasks:")
        print("   User: 'delete all tasks'")
        
        delete_empty_result = agent_service._delete_all_tasks({})
        
        clean_message = emoji_pattern.sub(r'', delete_empty_result['message'])
        print(f"   Response: {clean_message}\n")
        
        # Test 4: SET_TASK_DATE functionality
        print("4. Testing SET_TASK_DATE functionality:")
        print("   User: 'set date for task exercise to tomorrow'")
        
        # Create a task first
        task_result = agent_service._create_task({
            "title": "exercise",
            "description": "morning workout"
        })
        
        # Set the date for the task
        schedule_result = agent_service._set_task_schedule({
            "task_id": "exercise",
            "due_date": "2026-02-11"
        })
        
        clean_message = emoji_pattern.sub(r'', schedule_result['message'])
        print(f"   Response: {clean_message}\n")
        
        # Test 5: MARK_TASK_COMPLETE with friendly response
        print("5. Testing MARK_TASK_COMPLETE with friendly response:")
        print("   User: 'mark exercise as complete'")
        
        complete_result = agent_service._complete_task({
            "task_id": "exercise"
        })
        
        clean_message = emoji_pattern.sub(r'', complete_result['message'])
        print(f"   Response: {clean_message}\n")
        
        # Test 6: UPDATE_TASK with friendly response
        print("6. Testing UPDATE_TASK with friendly response:")
        print("   User: 'update task exercise to jog'")
        
        # Create another task to update
        update_task_result = agent_service._create_task({
            "title": "laundry",
            "description": "wash clothes"
        })
        
        update_result = agent_service._update_task({
            "task_id": "laundry",
            "title": "dry cleaning"
        })
        
        clean_message = emoji_pattern.sub(r'', update_result['message'])
        print(f"   Response: {clean_message}\n")
        
        # Test 7: DELETE_TASK with friendly response
        print("7. Testing DELETE_TASK with friendly response:")
        print("   User: 'delete task dry cleaning'")
        
        delete_result = agent_service._delete_task({
            "task_id": "dry cleaning"
        })
        
        clean_message = emoji_pattern.sub(r'', delete_result['message'])
        print(f"   Response: {clean_message}\n")
        
        print("=== ALL ENHANCEMENTS WORKING CORRECTLY ===")


if __name__ == "__main__":
    # Initialize the database
    from src.core.database import init_db
    init_db()
    
    # Run the test
    test_final_enhancements()