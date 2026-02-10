#!/usr/bin/env python3
"""
Test script to verify date functionality in task management.
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


def test_date_functionality():
    """Test the date functionality in task management."""
    print("Testing Date Functionality in Task Management...\n")
    
    # Set up test user
    user_id = setup_test_user()
    
    with Session(engine) as session:
        agent_service = AgentService(session, user_id=user_id)
        
        # Test 1: Create a task with a date
        print("Test 1: Creating a task with date information")
        create_result = agent_service._create_task({
            "title": "Operation",
            "description": "Task name operation",
            "due_date": "2026-02-23"
        })
        print(f"Result: {create_result}")
        
        # Verify the task was created with the due date
        stmt = select(Task).where(Task.user_id == user_id).order_by(Task.created_at.desc()).limit(1)
        task = session.exec(stmt).first()
        print(f"Task due date: {task.due_date}")
        
        # Test 2: Create a task with natural language date
        print("\nTest 2: Creating a task with natural language date")
        create_result2 = agent_service._create_task({
            "title": "Meeting",
            "description": "Team meeting",
            "due_date": "2026-03-15"
        })
        print(f"Result: {create_result2}")
        
        # Verify the task was created with the due date
        stmt = select(Task).where(Task.user_id == user_id).order_by(Task.created_at.desc()).limit(1)
        task2 = session.exec(stmt).first()
        print(f"Task due date: {task2.due_date}")
        
        # Test 3: Update a task with a new due date
        print("\nTest 3: Updating a task with a new due date")
        update_result = agent_service._update_task({
            "task_id": task.id,
            "due_date": "2026-03-01"
        })
        print(f"Update result: {update_result}")
        
        # Verify the task was updated with the new due date
        updated_task = session.get(Task, task.id)
        print(f"Updated task due date: {updated_task.due_date}")
        
        # Test 4: List tasks with due date filter
        print("\nTest 4: Listing tasks with due date filter")
        list_result = agent_service._list_tasks({
            "due_date": "2026-03"
        })
        print(f"Tasks due in March 2026: {list_result}")
        
        print("\nDate functionality testing completed!")


if __name__ == "__main__":
    # Initialize the database
    from src.core.database import init_db
    init_db()
    
    # Run the test
    test_date_functionality()