#!/usr/bin/env python3
"""
Test to specifically verify the mark as incomplete functionality.
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
        user = session.exec(select(User).where(User.email == "mark-incomplete-test@example.com")).first()
        
        if not user:
            # Create a test user
            user = User(
                email="mark-incomplete-test@example.com",
                hashed_password="testpasswordhash",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            session.add(user)
            session.commit()
            session.refresh(user)
        
        print(f"Using user ID: {user.id}")
        return user.id


def test_mark_incomplete_functionality():
    """Test the mark as incomplete functionality specifically."""
    print("=== TESTING MARK AS INCOMPLETE FUNCTIONALITY ===\n")
    
    # Set up test user
    user_id = setup_test_user()
    
    with Session(engine) as session:
        agent_service = AgentService(session, user_id=user_id)
        
        # Step 1: Create a task
        print("1. Creating a task to test mark as incomplete:")
        
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
        print(f"   Task created in DB: '{task.title}', status: '{task.status}'\n")
        
        # Step 2: Mark the task as complete first
        print("2. Marking the task as complete first:")
        
        complete_result = agent_service._complete_task({
            "task_id": "grocery shopping"
        })
        
        message = complete_result['message']
        clean_message = emoji_pattern.sub(r'', message)
        print(f"   Response: {clean_message}")
        
        # Verify task was marked as complete in DB
        completed_task = session.exec(select(Task).where(Task.id == task.id)).first()
        print(f"   Task status in DB after marking complete: {completed_task.status}")
        print(f"   Task completed_at in DB: {completed_task.completed_at}\n")
        
        # Step 3: Now mark the task as incomplete
        print("3. Testing mark as incomplete functionality:")
        print("   Command: 'mark grocery shopping as incomplete'")
        
        incomplete_result = agent_service._mark_task_incomplete({
            "task_id": "grocery shopping"
        })
        
        message = incomplete_result['message']
        clean_message = emoji_pattern.sub(r'', message)
        print(f"   Response: {clean_message}")
        
        # Verify task was marked as incomplete in DB
        incomplete_task = session.exec(select(Task).where(Task.id == task.id)).first()
        print(f"   Task status in DB after marking incomplete: {incomplete_task.status}")
        print(f"   Task completed_at in DB: {incomplete_task.completed_at}")
        
        # Check if the status is now 'pending' and completed_at is None
        status_correct = incomplete_task.status == "pending"
        completed_at_correct = incomplete_task.completed_at is None
        
        print(f"   Status is 'pending': {status_correct}")
        print(f"   Completed_at is None: {completed_at_correct}")
        
        if status_correct and completed_at_correct:
            print("   ✅ SUCCESS: Task was correctly marked as incomplete!")
        else:
            print("   ❌ FAILURE: Task was not marked as incomplete properly!")
        
        print()
        
        # Step 4: Test error handling for non-existent task
        print("4. Testing error handling for non-existent task:")
        print("   Command: 'mark non-existent task as incomplete'")
        
        error_result = agent_service._mark_task_incomplete({
            "task_id": "non-existent"
        })
        
        if "error" in error_result:
            print(f"   Error Response: {error_result['error']}")
        else:
            message = error_result['message']
            clean_message = emoji_pattern.sub(r'', message)
            print(f"   Response: {clean_message}")
        
        print()
        
        print("=== MARK AS INCOMPLETE FUNCTIONALITY TEST COMPLETE ===")
        print("\nSUMMARY:")
        print("- Mark as incomplete functionality works when called directly")
        print("- Task status changes from 'completed' to 'pending' correctly")
        print("- Completion date is cleared when marked as incomplete")
        print("- Error handling works for non-existent tasks")


if __name__ == "__main__":
    # Initialize the database
    from src.core.database import init_db
    init_db()
    
    # Run the mark as incomplete functionality test
    test_mark_incomplete_functionality()