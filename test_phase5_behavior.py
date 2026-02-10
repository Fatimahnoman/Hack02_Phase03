"""
Test script to verify Phase 5 behavior of the chatbot.
This script tests that the bot behaves exactly like Phase 5:
- When a user says "add my task ...", the task is created immediately
- No authentication required - uses default user
- Direct action mode without help-style replies
"""

import asyncio
import sys
import os

# Add the backend src directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend', 'src'))

from sqlmodel import create_engine, Session
from services.database_service import DatabaseService
from services.stateless_conversation_service import StatelessConversationService
from core.database import engine


def test_phase5_behavior():
    """Test that the chatbot behaves like Phase 5."""
    
    print("Testing Phase 5 behavior...")
    
    # Create a database session
    with Session(engine) as session:
        # Create database service
        db_service = DatabaseService(session)
        
        # Create stateless conversation service
        conversation_service = StatelessConversationService(db_service)
        
        # Test 1: Add a task without providing user_id (should use default user)
        print("\n1. Testing task creation without user_id:")
        result = asyncio.run(conversation_service.process_request(
            user_input="add my task Buy groceries",
            user_id=None  # No user_id provided
        ))
        print(f"Response: {result['response']}")
        print(f"Tool execution: {result['tool_execution_result']}")
        
        # Test 2: Add a task with invalid user_id (should use default user)
        print("\n2. Testing task creation with invalid user_id:")
        result = asyncio.run(conversation_service.process_request(
            user_input="add my task Walk the dog",
            user_id="invalid_user"  # Invalid user_id
        ))
        print(f"Response: {result['response']}")
        print(f"Tool execution: {result['tool_execution_result']}")
        
        # Test 3: Add a task with valid user_id
        print("\n3. Testing task creation with valid user_id:")
        result = asyncio.run(conversation_service.process_request(
            user_input="add my task Call mom",
            user_id="1"  # Valid user_id
        ))
        print(f"Response: {result['response']}")
        print(f"Tool execution: {result['tool_execution_result']}")
        
        # Test 4: List tasks
        print("\n4. Testing task listing:")
        result = asyncio.run(conversation_service.process_request(
            user_input="list my tasks",
            user_id="1"
        ))
        print(f"Response: {result['response']}")
        print(f"Tool execution: {result['tool_execution_result']}")
        
        # Test 5: Test direct action without help-style reply
        print("\n5. Testing direct action without help-style reply:")
        result = asyncio.run(conversation_service.process_request(
            user_input="add task Schedule meeting with team",
            user_id="1"
        ))
        print(f"Response: {result['response']}")
        print(f"Expected: Should be a direct confirmation, not a help message")
        
        print("\nPhase 5 behavior test completed!")


if __name__ == "__main__":
    test_phase5_behavior()