#!/usr/bin/env python3
"""
Test script to verify intent detection functionality.
This script tests the various CRUD operations for tasks.
"""

import asyncio
import sys
import os

# Add the backend src directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend', 'src'))

from sqlmodel import Session
from src.services.agent_service import AgentService
from src.core.database import engine
from src.models.user import User
from src.models.task import Task
from src.core.config import settings
from datetime import datetime
import uuid


def setup_test_user():
    """Set up a test user for testing purposes."""
    with Session(engine) as session:
        # Check if test user already exists
        user = session.query(User).filter(User.email == "test@example.com").first()
        
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


def test_intent_detection():
    """Test the intent detection functionality."""
    print("Testing Intent Detection for Task Management Operations...\n")
    
    # Set up test user
    user_id = setup_test_user()
    
    # Create agent service instance
    with Session(engine) as session:
        agent_service = AgentService(session, user_id=user_id)
        
        # Test cases for different intents
        test_cases = [
            {
                "input": "create a new task to buy groceries",
                "expected_action": "create_task",
                "description": "CREATE task intent"
            },
            {
                "input": "update my buy groceries task to buy makeup",
                "expected_action": "update_task", 
                "description": "UPDATE task intent"
            },
            {
                "input": "mark my buy groceries task as complete",
                "expected_action": "complete_task",
                "description": "MARK COMPLETE task intent"
            },
            {
                "input": "delete my buy groceries task",
                "expected_action": "delete_task",
                "description": "DELETE task intent"
            },
            {
                "input": "delete all tasks",
                "expected_action": "delete_all_tasks",
                "description": "DELETE ALL tasks intent"
            },
            {
                "input": "show me my tasks",
                "expected_action": "list_tasks",
                "description": "LIST tasks intent"
            }
        ]
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"Test {i}: {test_case['description']}")
            print(f"Input: \"{test_case['input']}\"")
            
            # Process the request
            result = agent_service.process_request(
                user_input=test_case['input'],
                conversation_history=[]
            )
            
            print(f"Response: {result['response']}")
            
            # Check if any tool was called
            if result['tool_calls']:
                tool_names = [call['name'] for call in result['tool_calls']]
                print(f"Tools called: {tool_names}")
            else:
                print("No tools called")
            
            print("-" * 50)
        
        print("\nIntent detection testing completed!")


if __name__ == "__main__":
    # Initialize the database
    from core.database import init_db
    init_db()
    
    # Run the test
    test_intent_detection()