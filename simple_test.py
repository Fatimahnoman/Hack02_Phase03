#!/usr/bin/env python3
"""
Simple test to verify the new delete_all_tasks functionality works correctly.
"""

import sys
import os
import uuid
from datetime import datetime

# Add the backend src directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend', 'src'))

from sqlmodel import Session, select
from src.services.agent_service import AgentService
from src.core.database import engine
from src.models.user import User
from src.models.task import Task


def setup_test_user():
    """Set up a test user for testing purposes."""
    with Session(engine) as session:
        # Check if test user already exists
        user = session.exec(select(User).where(User.email == "test@example.com")).first()
        
        if not user:
            # Create a test user
            user = User(
                email="test@example.com",
                hashed_password="testpasswordhash",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            session.add(user)
            session.commit()
            session.refresh(user)
        
        print(f"Using user ID: {user.id}")
        return user.id


def test_delete_all_tasks():
    """Test the delete_all_tasks functionality."""
    print("Testing delete_all_tasks functionality...\n")
    
    # Set up test user
    user_id = setup_test_user()
    
    with Session(engine) as session:
        agent_service = AgentService(session, user_id=user_id)
        
        # First, create some test tasks
        print("Creating test tasks...")
        for i in range(3):
            task_args = {
                "title": f"Test Task {i+1}",
                "description": f"This is test task number {i+1}",
                "priority": "medium"
            }
            result = agent_service._create_task(task_args)
            # Remove emojis from the message for console compatibility
            message = result['message']
            # Remove common emojis
            import re
            emoji_pattern = re.compile("["
                                   u"\U0001F600-\U0001F64F"  # emoticons
                                   u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                   u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                   u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                   u"\U00002702-\U000027B0"
                                   u"\U000024C2-\U0001F251"
                                   "]+", flags=re.UNICODE)
            clean_message = emoji_pattern.sub(r'', message)
            print(f"Created task: {clean_message}")
        
        # Verify tasks were created
        stmt = select(Task).where(Task.user_id == user_id)
        tasks = session.exec(stmt).all()
        print(f"Number of tasks before deletion: {len(tasks)}")
        
        # Test delete_all_tasks
        print("\nTesting delete_all_tasks...")
        delete_result = agent_service._delete_all_tasks({})
        print(f"Delete result: {delete_result}")
        
        # Verify tasks were deleted
        tasks_after = session.exec(stmt).all()
        print(f"Number of tasks after deletion: {len(tasks_after)}")
        
        if len(tasks_after) == 0:
            print("\nSUCCESS: All tasks were deleted successfully!")
        else:
            print(f"\nFAILURE: {len(tasks_after)} tasks remain after deletion!")
            
        # Clean up - recreate user if needed for further tests
        print("\nTest completed!")


def test_responses():
    """Test that the responses are appropriate for each operation."""
    print("\nTesting appropriate responses for each operation...\n")
    
    user_id = setup_test_user()
    
    with Session(engine) as session:
        agent_service = AgentService(session, user_id=user_id)
        
        # Test create task response
        print("1. Testing create task response:")
        create_result = agent_service._create_task({
            "title": "Buy groceries",
            "description": "Buy milk, bread, and eggs",
            "priority": "high"
        })
        # Remove emojis from the message for console compatibility
        message = create_result['message']
        import re
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
        
        # Test update task response
        print("\n2. Testing update task response:")
        # First get the task we just created
        stmt = select(Task).where(Task.user_id == user_id).order_by(Task.created_at.desc()).limit(1)
        task = session.exec(stmt).first()
        
        if task:
            update_result = agent_service._update_task({
                "task_id": task.id,
                "title": "Buy makeup",
                "description": "Buy lipstick, mascara, and foundation"
            })
            # Remove emojis from the message for console compatibility
        message = update_result['message']
        import re
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
        
        # Test complete task response
        print("\n3. Testing complete task response:")
        if task:
            complete_result = agent_service._complete_task({
                "task_id": task.id
            })
            # Remove emojis from the message for console compatibility
        message = complete_result['message']
        import re
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
        
        # Test delete task response
        print("\n4. Testing delete task response:")
        if task:
            # Create a new task to delete
            new_task_result = agent_service._create_task({
                "title": "Temporary task",
                "description": "This is a temporary task for testing",
                "priority": "low"
            })
            new_task_id = session.exec(select(Task).where(Task.user_id == user_id).order_by(Task.created_at.desc()).limit(1)).first().id
            
            delete_result = agent_service._delete_task({
                "task_id": new_task_id
            })
            # Remove emojis from the message for console compatibility
        message = delete_result['message']
        import re
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
        
        print("\nResponse testing completed!")


if __name__ == "__main__":
    # Initialize the database
    from src.core.database import init_db
    init_db()
    
    # Run the tests
    test_delete_all_tasks()
    test_responses()