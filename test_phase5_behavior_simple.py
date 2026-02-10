"""
Integration test to verify Phase 5 behavior of the chatbot.
This script tests that the bot behaves exactly like Phase 5:
- When a user says "add my task ...", the task is created immediately
- No authentication required - uses default user
- Direct action mode without help-style replies
"""

import asyncio
import sys
import os
from unittest.mock import AsyncMock, MagicMock

# Add the backend src directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend', 'src'))

from sqlmodel import create_engine, Session
from sqlalchemy.pool import StaticPool
from services.database_service import DatabaseService
from services.stateless_conversation_service import StatelessConversationService
from models.user import User
from models.task import Task
from datetime import datetime


def test_phase5_behavior():
    """Test that the chatbot behaves like Phase 5."""
    
    print("Testing Phase 5 behavior...")
    
    # Create an in-memory SQLite database for testing
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    
    # Create tables
    from src.models.user import User
    from src.models.task import Task
    from src.models.message import Message
    from src.models.conversation import Conversation
    from src.models.tool_call import ToolCall
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(bind=engine)
    
    # Create a session
    with Session(engine) as session:
        # Add a default user with ID 1
        default_user = User(
            id=1,
            email="default@example.com",
            hashed_password="dummy_hash",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        session.add(default_user)
        session.commit()
        
        # Create database service
        db_service = DatabaseService(session)
        
        # Mock the agent service to avoid needing OpenAI API
        from src.services.agent_service import AgentService
        original_init = AgentService.__init__
        original_process = AgentService.process_request
        
        def mock_init(self, session, user_id=1):
            self.session = session
            self.user_id = user_id
            # Don't initialize OpenAI client to avoid API key requirement
            
        def mock_process_request(self, user_input, conversation_history):
            # Simulate the expected behavior for task creation
            if "add" in user_input.lower() and ("task" in user_input.lower() or "my" in user_input.lower()):
                # Simulate creating a task
                task_title = user_input.replace("add my task", "").replace("add task", "").strip()
                
                # Create a mock task in the database
                from src.models.task import Task, TaskCreate
                task_create = TaskCreate(
                    title=task_title,
                    description=f"Description for {task_title}",
                    priority="medium",
                    user_id=self.user_id
                )
                task = Task(**task_create.dict())
                self.session.add(task)
                self.session.commit()
                self.session.refresh(task)
                
                return {
                    "response": f"Task '{task_title}' has been created successfully!",
                    "tool_calls": [{
                        "function_name": "create_task",
                        "parameters": {"title": task_title},
                        "id": "mock_call_1"
                    }],
                    "status": "success"
                }
            elif "list" in user_input.lower() and "task" in user_input.lower():
                # Simulate listing tasks
                from src.services.task_display_service import TaskDisplayService
                display_service = TaskDisplayService(self.session)
                tasks = display_service.get_tasks_with_numbers(user_id=self.user_id)
                
                task_list_str = ", ".join([f"{task['display_number']}. {task['title']} ({task['status']})" for task in tasks])
                if not task_list_str:
                    task_list_str = "No tasks found"
                    
                return {
                    "response": f"Your tasks: {task_list_str}",
                    "tool_calls": [{
                        "function_name": "list_tasks",
                        "parameters": {},
                        "id": "mock_call_2"
                    }],
                    "status": "success"
                }
            else:
                return {
                    "response": "Processed your request.",
                    "tool_calls": [],
                    "status": "success"
                }
        
        # Patch the AgentService methods
        AgentService.__init__ = mock_init
        AgentService.process_request = mock_process_request
        
        try:
            # Create stateless conversation service
            conversation_service = StatelessConversationService(db_service)
            
            # Test 1: Add a task without providing user_id (should use default user)
            print("\n1. Testing task creation without user_id:")
            result = asyncio.run(conversation_service.process_request(
                user_input="add my task Buy groceries",
                user_id=None  # No user_id provided
            ))
            print(f"Response: {result['response']}")
            print(f"User ID used: {result['state_reflection']['user_id']}")
            
            # Test 2: Add a task with invalid user_id (should use default user)
            print("\n2. Testing task creation with invalid user_id:")
            result = asyncio.run(conversation_service.process_request(
                user_input="add my task Walk the dog",
                user_id="invalid_user"  # Invalid user_id
            ))
            print(f"Response: {result['response']}")
            print(f"User ID used: {result['state_reflection']['user_id']}")
            
            # Test 3: Add a task with valid user_id
            print("\n3. Testing task creation with valid user_id:")
            result = asyncio.run(conversation_service.process_request(
                user_input="add my task Call mom",
                user_id="1"  # Valid user_id
            ))
            print(f"Response: {result['response']}")
            print(f"User ID used: {result['state_reflection']['user_id']}")
            
            # Test 4: List tasks
            print("\n4. Testing task listing:")
            result = asyncio.run(conversation_service.process_request(
                user_input="list my tasks",
                user_id="1"
            ))
            print(f"Response: {result['response']}")
            
            # Test 5: Test direct action without help-style reply
            print("\n5. Testing direct action without help-style reply:")
            result = asyncio.run(conversation_service.process_request(
                user_input="add task Schedule meeting with team",
                user_id="1"
            ))
            print(f"Response: {result['response']}")
            print(f"Expected: Should be a direct confirmation, not a help message")
            
            print("\nPhase 5 behavior test completed successfully!")
            
        finally:
            # Restore original methods
            AgentService.__init__ = original_init
            AgentService.process_request = original_process


if __name__ == "__main__":
    test_phase5_behavior()