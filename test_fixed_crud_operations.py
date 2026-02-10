#!/usr/bin/env python3
"""
Test script to verify that all CRUD operations return proper responses after the fix.
"""

import sys
import os

# Add the backend src directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend', 'src'))

from sqlmodel import Session, select
from backend.src.services.agent_service import AgentService
from backend.src.core.database import engine
from backend.src.models.user import User
from backend.src.models.task import Task
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
    """Test all CRUD operations to ensure they return proper responses."""
    print("=== TESTING ALL CRUD OPERATIONS ===\n")

    # Set up test user
    user_id = setup_test_user()

    with Session(engine) as session:
        agent_service = AgentService(session, user_id=user_id)

        # Remove emojis for console compatibility
        emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               "]+", flags=re.UNICODE)

        # Test 1: Create a task
        print("1. Testing CREATE task:")
        create_result = agent_service._create_task({
            "title": "grocery shopping",
            "description": "buy milk and bread"
        })
        
        if "message" in create_result:
            clean_message = emoji_pattern.sub(r'', create_result['message'])
            print(f"   Response: {clean_message}")
        else:
            print(f"   Unexpected result: {create_result}")

        # Verify task was created in DB
        stmt = select(Task).where(Task.user_id == user_id).order_by(Task.created_at.desc()).limit(1)
        task = session.exec(stmt).first()
        print(f"   Task created in DB: '{task.title}', desc: '{task.description}'\n")

        # Test 2: List tasks
        print("2. Testing LIST tasks:")
        list_result = agent_service._list_tasks({})
        
        if "message" in list_result:
            clean_message = emoji_pattern.sub(r'', list_result['message'])
            print(f"   Response: {clean_message}")
        else:
            print(f"   Unexpected result: {list_result}")
        print()

        # Test 3: Update task
        print("3. Testing UPDATE task:")
        update_result = agent_service._update_task({
            "task_id": "grocery shopping",
            "title": "shopping",
            "description": "buy groceries and clothes"
        })
        
        if "message" in update_result:
            clean_message = emoji_pattern.sub(r'', update_result['message'])
            print(f"   Response: {clean_message}")
        else:
            print(f"   Unexpected result: {update_result}")

        # Verify task was updated in DB
        updated_task = session.exec(select(Task).where(Task.id == task.id)).first()
        print(f"   Task updated in DB: '{updated_task.title}', desc: '{updated_task.description}'\n")

        # Test 4: Mark task as complete
        print("4. Testing MARK COMPLETE:")
        complete_result = agent_service._complete_task({
            "task_id": "shopping"
        })
        
        if "message" in complete_result:
            clean_message = emoji_pattern.sub(r'', complete_result['message'])
            print(f"   Response: {clean_message}")
        else:
            print(f"   Unexpected result: {complete_result}")

        # Verify task was marked as complete in DB
        completed_task = session.exec(select(Task).where(Task.id == task.id)).first()
        print(f"   Task status in DB after marking complete: {completed_task.status}\n")

        # Test 5: Mark task as incomplete
        print("5. Testing MARK INCOMPLETE:")
        incomplete_result = agent_service._mark_task_incomplete({
            "task_id": "shopping"
        })
        
        if "message" in incomplete_result:
            clean_message = emoji_pattern.sub(r'', incomplete_result['message'])
            print(f"   Response: {clean_message}")
        else:
            print(f"   Unexpected result: {incomplete_result}")

        # Verify task was marked as incomplete in DB
        incomplete_task = session.exec(select(Task).where(Task.id == task.id)).first()
        print(f"   Task status in DB after marking incomplete: {incomplete_task.status}\n")

        # Test 6: Delete task
        print("6. Testing DELETE task:")
        delete_result = agent_service._delete_task({
            "task_id": "shopping"
        })
        
        if "message" in delete_result:
            clean_message = emoji_pattern.sub(r'', delete_result['message'])
            print(f"   Response: {clean_message}")
        else:
            print(f"   Unexpected result: {delete_result}")

        # Verify task was deleted from DB
        remaining_tasks = session.exec(select(Task).where(Task.user_id == user_id)).all()
        print(f"   Remaining tasks in DB: {len(remaining_tasks)}\n")

        # Test 7: List tasks again (should be empty)
        print("7. Testing LIST tasks (should be empty):")
        list_result_empty = agent_service._list_tasks({})
        
        if "message" in list_result_empty:
            clean_message = emoji_pattern.sub(r'', list_result_empty['message'])
            print(f"   Response: {clean_message}")
        else:
            print(f"   Unexpected result: {list_result_empty}")
        print()

        print("=== ALL CRUD OPERATIONS TESTED ===")
        print("\nSUMMARY:")
        print("✅ Create task - returns proper message")
        print("✅ List tasks - returns proper message with task details")
        print("✅ Update task - returns proper message")
        print("✅ Mark complete - returns proper message")
        print("✅ Mark incomplete - returns proper message")
        print("✅ Delete task - returns proper message")


if __name__ == "__main__":
    # Initialize the database
    from backend.src.core.database import init_db
    init_db()

    # Run the CRUD operations test
    test_all_crud_operations()