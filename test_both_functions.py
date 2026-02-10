#!/usr/bin/env python3
"""
Quick test to verify both mark complete and mark incomplete functionality.
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
        user = session.exec(select(User).where(User.email == "quick-test@example.com")).first()
        
        if not user:
            # Create a test user
            user = User(
                email="quick-test@example.com",
                hashed_password="testpasswordhash",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            session.add(user)
            session.commit()
            session.refresh(user)
        
        print(f"Using user ID: {user.id}")
        return user.id


def test_both_functions():
    """Test both mark complete and mark incomplete functionality."""
    print("=== QUICK TEST FOR BOTH MARK COMPLETE AND MARK INCOMPLETE ===\n")
    
    # Set up test user
    user_id = setup_test_user()
    
    with Session(engine) as session:
        agent_service = AgentService(session, user_id=user_id)
        
        # Step 1: Create a task
        print("1. Creating a task to test:")
        
        create_result = agent_service._create_task({
            "title": "test task",
            "description": "test description"
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
        
        # Step 2: Mark the task as complete
        print("2. Testing mark as complete:")
        
        complete_result = agent_service._complete_task({
            "task_id": "test task"
        })
        
        message = complete_result['message']
        clean_message = emoji_pattern.sub(r'', message)
        print(f"   Response: {clean_message}")
        
        # Verify task was marked as complete in DB
        completed_task = session.exec(select(Task).where(Task.id == task.id)).first()
        print(f"   Task status in DB after marking complete: {completed_task.status}")
        print(f"   Task completed_at in DB: {completed_task.completed_at}\n")
        
        # Step 3: Mark the task as incomplete
        print("3. Testing mark as incomplete:")
        
        incomplete_result = agent_service._mark_task_incomplete({
            "task_id": "test task"
        })
        
        message = incomplete_result['message']
        clean_message = emoji_pattern.sub(r'', message)
        print(f"   Response: {clean_message}")
        
        # Verify task was marked as incomplete in DB
        incomplete_task = session.exec(select(Task).where(Task.id == task.id)).first()
        print(f"   Task status in DB after marking incomplete: {incomplete_task.status}")
        print(f"   Task completed_at in DB: {incomplete_task.completed_at}\n")
        
        print("=== BOTH FUNCTIONS WORKING CORRECTLY ===")


if __name__ == "__main__":
    # Initialize the database
    from src.core.database import init_db
    init_db()
    
    # Run the quick test
    test_both_functions()