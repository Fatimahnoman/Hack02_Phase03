#!/usr/bin/env python3
"""
Test script to verify date functionality in task management with simulated user input.
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


def test_date_extraction():
    """Test the date extraction functionality in task creation."""
    print("Testing Date Extraction in Task Creation...\n")
    
    # Set up test user
    user_id = setup_test_user()
    
    with Session(engine) as session:
        agent_service = AgentService(session, user_id=user_id)
        
        # Test: Simulate user saying "add my task name operation is on 23 feb 2026"
        print("Simulating user input: 'add task name operation is on 23 feb 2026'")
        
        # This simulates how the AI would call the create_task function
        # based on the user's natural language input
        task_args = {
            "title": "operation",  # The AI would extract "operation" as the task name
            "description": "Task name operation Scheduled for: 23 feb 2026"  # Date info goes in description
        }
        
        create_result = agent_service._create_task(task_args)
        
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
        print(f"Result: {clean_message}")
        
        # Verify the task was created with the due date extracted from the description
        stmt = select(Task).where(Task.user_id == user_id).order_by(Task.created_at.desc()).limit(1)
        task = session.exec(stmt).first()
        print(f"Task title: {task.title}")
        print(f"Task description: {task.description}")
        print(f"Task due date: {task.due_date}")
        
        print("\nDate extraction testing completed!")


def test_list_with_date_filters():
    """Test listing tasks with date filters."""
    print("\nTesting List Tasks with Date Filters...\n")
    
    user_id = setup_test_user()
    
    with Session(engine) as session:
        agent_service = AgentService(session, user_id=user_id)
        
        # Create a few tasks with different due dates
        print("Creating tasks with different due dates...")
        
        # Task 1: Due today
        agent_service._create_task({
            "title": "Morning Meeting",
            "description": "Team standup",
            "due_date": datetime.now().strftime('%Y-%m-%d')
        })
        
        # Task 2: Due tomorrow
        tomorrow = datetime.now().replace(day=datetime.now().day + 1)
        agent_service._create_task({
            "title": "Submit Report",
            "description": "Monthly report submission",
            "due_date": tomorrow.strftime('%Y-%m-%d')
        })
        
        # List tasks due today
        print("\nListing tasks due 'today':")
        today_tasks = agent_service._list_tasks({"due_date": "today"})
        print(f"Found {len(today_tasks['tasks'])} tasks due today")
        
        # List tasks due this week
        print("\nListing tasks due 'this week':")
        week_tasks = agent_service._list_tasks({"due_date": "this week"})
        print(f"Found {len(week_tasks['tasks'])} tasks due this week")
        
        print("\nList with date filters testing completed!")


if __name__ == "__main__":
    # Initialize the database
    from src.core.database import init_db
    init_db()
    
    # Run the tests
    test_date_extraction()
    test_list_with_date_filters()