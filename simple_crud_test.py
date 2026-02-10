#!/usr/bin/env python3
"""
Simple test to verify that the chat functionality works properly with the updated code.
"""

import sys
import os

# Add the backend src directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend', 'src'))

from sqlmodel import Session
from backend.src.services.agent_service import AgentService
from backend.src.core.database import engine
from backend.src.models.user import User
from datetime import datetime


def setup_test_user():
    """Set up a test user for testing purposes."""
    with Session(engine) as session:
        # Check if test user already exists
        user = session.query(User).filter(User.email == "chat-test@example.com").first()

        if not user:
            # Create a test user
            user = User(
                email="chat-test@example.com",
                hashed_password="testpasswordhash",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            session.add(user)
            session.commit()
            session.refresh(user)

        print(f"Using user ID: {user.id}")
        return user.id


def test_chat_processing():
    """Test the chat processing functionality with various CRUD operations."""
    print("=== TESTING CHAT PROCESSING WITH CRUD OPERATIONS ===\n")

    # Set up test user
    user_id = setup_test_user()

    with Session(engine) as session:
        agent_service = AgentService(session, user_id=user_id)

        # Test various chat inputs that should trigger CRUD operations
        test_inputs = [
            "Add a task named 'Test Task' with description 'Testing CRUD operations'",
            "What are my tasks?",
            "Update 'Test Task' to 'Updated Task' with description 'Updated description'",
            "Mark 'Updated Task' as complete",
            "Mark 'Updated Task' as incomplete",
            "Delete the task 'Updated Task'",
            "What are my tasks now?"
        ]

        for i, user_input in enumerate(test_inputs, 1):
            print(f"{i}. Processing: '{user_input}'")
            
            try:
                result = agent_service.process_request(
                    user_input=user_input,
                    conversation_history=[]
                )
                
                response = result.get("response", "No response received")
                print(f"   Response: {response}")
                
                # Check if any tool calls were made
                tool_calls = result.get("tool_calls", [])
                if tool_calls:
                    print(f"   Tool calls made: {[call['name'] for call in tool_calls]}")
                
                print()
            except Exception as e:
                print(f"   Error processing input: {str(e)}\n")

        print("=== CHAT PROCESSING TEST COMPLETED ===")


if __name__ == "__main__":
    # Initialize the database
    from backend.src.core.database import init_db
    init_db()

    # Run the chat processing test
    test_chat_processing()