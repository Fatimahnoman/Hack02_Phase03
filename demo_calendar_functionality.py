#!/usr/bin/env python3
"""
Final demonstration of the complete calendar/date functionality.
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
from datetime import datetime, timedelta
import uuid
import re


def setup_test_user():
    """Set up a test user for testing purposes."""
    with Session(engine) as session:
        # Check if test user already exists
        user = session.exec(select(User).where(User.email == "demo@example.com")).first()
        
        if not user:
            # Create a test user
            user = User(
                email="demo@example.com",
                hashed_password="demopasswordhash",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            session.add(user)
            session.commit()
            session.refresh(user)
        
        print(f"Using user ID: {user.id}")
        return user.id


def demo_calendar_functionality():
    """Demonstrate the complete calendar functionality."""
    print("=== DEMONSTRATING CALENDAR FUNCTIONALITY ===\n")
    
    # Set up test user
    user_id = setup_test_user()
    
    with Session(engine) as session:
        agent_service = AgentService(session, user_id=user_id)
        
        print("1. User says: 'add my task name operation is on 23 feb 2026'")
        print("   Bot should recognize the date and create a task with due date")
        
        # Simulate how the AI would process this request
        task_args = {
            "title": "operation",
            "description": "Task name operation Scheduled for: 23 feb 2026"
        }
        
        result = agent_service._create_task(task_args)
        print(f"   Response: {result['message']}\n")
        
        # Verify the task was created with the due date
        stmt = select(Task).where(Task.user_id == user_id).order_by(Task.created_at.desc()).limit(1)
        task = session.exec(stmt).first()
        print(f"   Task created: '{task.title}'")
        print(f"   Due date: {task.due_date}\n")
        
        print("2. User says: 'add meeting with team on march 15th'")
        print("   Bot should recognize the date and create a task with due date")
        
        task_args2 = {
            "title": "meeting with team",
            "description": "Meeting scheduled for: march 15th"
        }
        
        result2 = agent_service._create_task(task_args2)
        print(f"   Response: {result2['message']}\n")
        
        # Verify the task was created with the due date
        stmt = select(Task).where(Task.user_id == user_id).order_by(Task.created_at.desc()).limit(1)
        task2 = session.exec(stmt).first()
        print(f"   Task created: '{task2.title}'")
        print(f"   Due date: {task2.due_date}\n")
        
        print("3. User says: 'what tasks do I have this week?'")
        print("   Bot should list tasks due this week")
        
        list_result = agent_service._list_tasks({"due_date": "this week"})
        print(f"   Found {len(list_result['tasks'])} tasks due this week:")
        for t in list_result['tasks']:
            print(f"     - {t['title']} (due: {t['due_date']})")
        print()
        
        print("4. User says: 'update my operation task to be on march 20th'")
        print("   Bot should update the due date of the existing task")
        
        update_result = agent_service._update_task({
            "task_id": task.id,
            "due_date": "2026-03-20"
        })
        print(f"   Response: {update_result['message']}\n")
        
        # Verify the task was updated
        updated_task = session.get(Task, task.id)
        print(f"   Task updated: '{updated_task.title}'")
        print(f"   New due date: {updated_task.due_date}\n")
        
        print("5. User says: 'show me tasks due on 23 feb 2026'")
        print("   Bot should list tasks due on that specific date")
        
        specific_date_result = agent_service._list_tasks({"due_date": "2026-02-23"})
        print(f"   Found {len(specific_date_result['tasks'])} tasks due on 2026-02-23:")
        for t in specific_date_result['tasks']:
            print(f"     - {t['title']} (due: {t['due_date']})")
        print()
        
        print("=== CALENDAR FUNCTIONALITY DEMONSTRATED SUCCESSFULLY ===")


if __name__ == "__main__":
    # Initialize the database
    from src.core.database import init_db
    init_db()
    
    # Run the demo
    demo_calendar_functionality()