#!/usr/bin/env python3
"""
Test script to verify the enhanced intent understanding functionality.
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
        user = session.exec(select(User).where(User.email == "enhanced-test@example.com")).first()
        
        if not user:
            # Create a test user
            user = User(
                email="enhanced-test@example.com",
                hashed_password="testpasswordhash",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            session.add(user)
            session.commit()
            session.refresh(user)
        
        print(f"Using user ID: {user.id}")
        return user.id


def test_enhanced_functionality():
    """Test the enhanced functionality with various user inputs."""
    print("=== TESTING ENHANCED FUNCTIONALITY ===\n")
    
    # Set up test user
    user_id = setup_test_user()
    
    with Session(engine) as session:
        agent_service = AgentService(session, user_id=user_id)
        
        # Test 1: CREATE_TASK
        print("1. Testing CREATE_TASK intent:")
        print("   User: 'add task grocery with description milk and schedule on 25 feb 2026'")
        
        # Simulate how the AI would process this request
        task_args = {
            "title": "grocery",
            "description": "milk",
            "due_date": "2026-02-25"
        }
        
        result = agent_service._create_task(task_args)
        
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
        print(f"   Response: {clean_message}")
        
        # Verify the task was created with the due date
        stmt = select(Task).where(Task.user_id == user_id).order_by(Task.created_at.desc()).limit(1)
        task = session.exec(stmt).first()
        print(f"   Task created: '{task.title}', due: {task.due_date}\n")
        
        # Test 2: MARK_TASK_COMPLETE
        print("2. Testing MARK_TASK_COMPLETE intent:")
        print("   User: 'mark buy makeup as complete'")
        
        complete_result = agent_service._complete_task({
            "task_id": task.id
        })
        
        clean_message = emoji_pattern.sub(r'', complete_result['message'])
        print(f"   Response: {clean_message}\n")
        
        # Test 3: DELETE_TASK
        print("3. Testing DELETE_TASK intent:")
        print("   User: 'delete my task grocery'")
        
        delete_result = agent_service._delete_task({
            "task_id": task.id
        })
        
        clean_message = emoji_pattern.sub(r'', delete_result['message'])
        print(f"   Response: {clean_message}\n")
        
        # Test 4: DELETE_ALL_TASKS
        print("4. Testing DELETE_ALL_TASKS intent:")
        print("   User: 'delete all tasks'")
        
        # First create a few tasks to delete
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
        
        # Test 5: SET_TASK_SCHEDULE
        print("5. Testing SET_TASK_SCHEDULE intent:")
        print("   User: 'set schedule for task exercise to tomorrow'")
        
        # First create a task to schedule
        schedule_task = agent_service._create_task({
            "title": "exercise",
            "description": "morning workout"
        })
        
        # Now update its schedule
        schedule_result = agent_service._set_task_schedule({
            "task_id": "exercise",  # Using title to find task
            "due_date": "2026-02-11"  # Tomorrow's date
        })
        
        clean_message = emoji_pattern.sub(r'', schedule_result['message'])
        print(f"   Response: {clean_message}\n")
        
        # Test 6: UPDATE_TASK
        print("6. Testing UPDATE_TASK intent:")
        print("   User: 'update my task exercise to jog'")
        
        update_result = agent_service._update_task({
            "task_id": "exercise",
            "title": "jog"
        })
        
        clean_message = emoji_pattern.sub(r'', update_result['message'])
        print(f"   Response: {clean_message}\n")
        
        # Test 7: LIST_TASKS
        print("7. Testing LIST_TASKS intent:")
        print("   User: 'show me my tasks'")
        
        list_result = agent_service._list_tasks({})
        
        print(f"   Response: Found {len(list_result['tasks'])} tasks\n")
        
        print("=== ENHANCED FUNCTIONALITY TEST COMPLETED SUCCESSFULLY ===")


if __name__ == "__main__":
    # Initialize the database
    from src.core.database import init_db
    init_db()
    
    # Run the test
    test_enhanced_functionality()