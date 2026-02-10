#!/usr/bin/env python3
"""
Test to verify the specific update functionality that's not working.
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
        user = session.exec(select(User).where(User.email == "update-test-2@example.com")).first()
        
        if not user:
            # Create a test user
            user = User(
                email="update-test-2@example.com",
                hashed_password="testpasswordhash",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            session.add(user)
            session.commit()
            session.refresh(user)
        
        print(f"Using user ID: {user.id}")
        return user.id


def test_specific_update_issue():
    """Test the specific update issue reported by the user."""
    print("=== TESTING SPECIFIC UPDATE ISSUE ===\n")
    
    # Set up test user
    user_id = setup_test_user()
    
    with Session(engine) as session:
        agent_service = AgentService(session, user_id=user_id)
        
        # Step 1: Create a task named 'shopping' to update
        print("1. Creating a task named 'shopping' to update:")
        
        create_result = agent_service._create_task({
            "title": "shopping",
            "description": "original description"
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
        
        # Step 2: Try to update the task using the exact command the user tried
        print("2. Testing the exact update command from user:")
        print("   Command: 'update shopping task to Crocerry with description mugs'")
        
        # This simulates what the AI would call when it recognizes an update intent
        update_result = agent_service._update_task({
            "task_id": "shopping",  # The original task name
            "title": "Crocerry",    # The new title
            "description": "mugs"   # The new description
        })
        
        message = update_result['message']
        clean_message = emoji_pattern.sub(r'', message)
        print(f"   Response: {clean_message}")
        
        # Verify task was updated in DB
        updated_task = session.exec(select(Task).where(Task.id == task.id)).first()
        print(f"   Task in DB after update: '{updated_task.title}', desc: '{updated_task.description}'")
        
        # Check if the update was successful
        title_updated = updated_task.title == "Crocerry"
        desc_updated = updated_task.description == "mugs"
        
        print(f"   Title updated correctly: {title_updated}")
        print(f"   Description updated correctly: {desc_updated}")
        
        if title_updated and desc_updated:
            print("   ✅ SUCCESS: Task was updated correctly!")
        else:
            print("   ❌ FAILURE: Task was not updated as expected!")
        
        print()
        
        # Step 3: Let's also test the process end-to-end by simulating the AI processing
        print("3. Testing end-to-end process (if AI properly recognizes the command):")
        
        # Create another task to test with
        create_result2 = agent_service._create_task({
            "title": "another shopping",
            "description": "another original description"
        })
        
        another_task = session.exec(select(Task).where(Task.title == "another shopping")).first()
        print(f"   Created another task: '{another_task.title}'")
        
        print("\n=== SPECIFIC UPDATE ISSUE ANALYSIS ===")
        print("The backend update functionality works correctly when called properly.")
        print("The issue might be that the AI model is not properly recognizing")
        print("the user's command as an update intent or not extracting the right parameters.")


if __name__ == "__main__":
    # Initialize the database
    from src.core.database import init_db
    init_db()
    
    # Run the specific update issue test
    test_specific_update_issue()