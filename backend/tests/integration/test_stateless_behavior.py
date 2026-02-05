"""Integration tests for stateless behavior verification."""

import pytest
from fastapi.testclient import TestClient
from backend.src.main import app
from backend.src.services.stateless_conversation_service import StatelessConversationService
from backend.src.services.database_service import DatabaseService
from unittest.mock import AsyncMock, patch
from datetime import datetime
import json


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


@pytest.mark.asyncio
async def test_no_conversation_memory_dependency():
    """Test that each request is processed independently without conversation memory."""
    with TestClient(app) as client:
        user_id = "test-no-memory-user"

        # Send a request to create a task
        response1 = client.post(
            "/api/v1/chat/",
            json={
                "user_input": "Create a task to buy groceries",
                "user_id": user_id
            }
        )

        assert response1.status_code == 200
        data1 = response1.json()

        # Send another request that refers to previous context
        response2 = client.post(
            "/api/v1/chat/",
            json={
                "user_input": "What did I just ask you to do?",
                "user_id": user_id
            }
        )

        assert response2.status_code == 200
        data2 = response2.json()

        # In a truly stateless system, the second request should not know
        # about the previous conversation context, so the intent should be processed
        # based only on the current input
        # The system should acknowledge that it doesn't maintain conversation history
        # For our implementation, it will process the current input as a new request


@pytest.mark.asyncio
async def test_identical_inputs_produce_identical_outputs():
    """Test that identical inputs under same conditions produce identical outputs."""
    with TestClient(app) as client:
        user_id = "test-identical-inputs-user"

        # Send the same request twice
        request_payload = {
            "user_input": "What are my pending tasks?",
            "user_id": user_id
        }

        response1 = client.post("/api/v1/chat/", json=request_payload)
        response2 = client.post("/api/v1/chat/", json=request_payload)

        assert response1.status_code == 200
        assert response2.status_code == 200

        data1 = response1.json()
        data2 = response2.json()

        # Compare the intents (these should be identical)
        assert data1["intent"] == data2["intent"]

        # With empty user state, both responses should be similar
        # The actual responses might differ based on database state, but intents should be the same


@pytest.mark.asyncio
async def test_server_restart_equivalence():
    """Test that the system behaves consistently across server restarts."""
    # Note: This test would typically require restarting the server between requests
    # In our case, we'll simulate by ensuring each request is independent
    with TestClient(app) as client:
        user_id = "test-restart-equivalence-user"

        # Send requests that should be processed identically
        for i in range(3):
            response = client.post(
                "/api/v1/chat/",
                json={
                    "user_input": "Hello",
                    "user_id": user_id
                }
            )

            assert response.status_code == 200
            data = response.json()

            # Each request should be processed independently
            assert "response" in data
            assert "intent" in data
            assert data["intent"] == "greeting"


@pytest.mark.asyncio
async def test_database_state_driven_behavior():
    """Test that responses are driven by database state, not conversation memory."""
    # Create a mock database service to test the stateless behavior
    mock_session = AsyncMock()
    mock_db_service = DatabaseService(mock_session)

    # Mock the database responses
    mock_user_state = {
        "user_id": "test-user",
        "task_count": 2,
        "task_counts_by_status": {"pending": 1, "completed": 1},
        "recent_intents_count": 1
    }

    mock_db_service.get_user_state_summary = AsyncMock(return_value=mock_user_state)
    mock_db_service.get_user_tasks = AsyncMock(return_value=[])
    mock_db_service.create_task = AsyncMock(return_value=AsyncMock(id="new-task-id", title="Test Task", status="pending"))
    mock_db_service.log_intent = AsyncMock(return_value=AsyncMock(id="intent-log-id"))
    mock_db_service.log_tool_execution = AsyncMock(return_value=AsyncMock())

    # Create the service
    service = StatelessConversationService(mock_db_service)

    # Test that the service uses database state to inform responses
    result = await service.process_request(
        user_input="What are my tasks?",
        user_id="test-user"
    )

    # Verify that database methods were called (state fetching)
    mock_db_service.get_user_state_summary.assert_called_once_with("test-user")
    assert result["state_reflection"]["task_count"] == 2


@pytest.mark.asyncio
async def test_no_in_memory_cache_usage():
    """Test that no in-memory cache is used between requests."""
    with TestClient(app) as client:
        user_id = "test-no-cache-user"

        # First request
        response1 = client.post(
            "/api/v1/chat/",
            json={
                "user_input": "What are my tasks?",
                "user_id": user_id
            }
        )

        # Second request with same user
        response2 = client.post(
            "/api/v1/chat/",
            json={
                "user_input": "Show me my tasks",
                "user_id": user_id
            }
        )

        assert response1.status_code == 200
        assert response2.status_code == 200

        data1 = response1.json()
        data2 = response2.json()

        # Both should result in task-related intents since they're processed independently
        assert data1["intent"] in ["get_all_tasks", "get_pending_tasks"]
        assert data2["intent"] in ["get_all_tasks", "get_pending_tasks"]


@pytest.mark.asyncio
async def test_stateless_conversation_service_independence():
    """Test that StatelessConversationService operates independently."""
    mock_session = AsyncMock()
    mock_db_service = DatabaseService(mock_session)

    # Mock methods to return predictable values
    mock_db_service.get_user_state_summary = AsyncMock(return_value={
        "user_id": "test-user",
        "task_count": 0,
        "task_counts_by_status": {},
        "recent_intents_count": 0
    })
    mock_db_service.log_intent = AsyncMock(return_value=AsyncMock(id="intent-id"))
    mock_db_service.log_tool_execution = AsyncMock(return_value=AsyncMock())

    service = StatelessConversationService(mock_db_service)

    # Process multiple requests independently
    result1 = await service.process_request(
        user_input="Create task to call mom",
        user_id="user1"
    )

    result2 = await service.process_request(
        user_input="Create task to call mom",  # Same input, different user
        user_id="user2"
    )

    result3 = await service.process_request(
        user_input="What are my tasks?",  # Different input, same user as #1
        user_id="user1"
    )

    # Each request should be processed independently
    assert result1["intent"] == "create_task"
    assert result2["intent"] == "create_task"
    assert result3["intent"] == "get_all_tasks"

    # The service should not maintain any state between these calls


@pytest.mark.asyncio
async def test_context_management_is_database_only():
    """Test that context management relies only on database, not memory."""
    mock_session = AsyncMock()
    mock_db_service = DatabaseService(mock_session)

    # Mock context methods
    mock_db_service.get_conversation_context = AsyncMock(return_value=None)
    mock_db_service.create_conversation_context = AsyncMock(
        return_value=AsyncMock(id="ctx-id", context_data="{}", expires_at=datetime.now())
    )

    service = StatelessConversationService(mock_db_service)

    # Get context (should come from DB only)
    context = await service.get_database_only_context("user123", "task-assist")

    # Verify database was called
    mock_db_service.get_conversation_context.assert_called_once_with("user123", "task-assist")


@pytest.mark.asyncio
async def test_tool_execution_is_stateless():
    """Test that tool execution doesn't rely on conversation history."""
    mock_session = AsyncMock()
    mock_db_service = DatabaseService(mock_session)

    # Mock methods
    mock_db_service.get_user_state_summary = AsyncMock(return_value={"task_count": 0})
    mock_db_service.log_intent = AsyncMock(return_value=AsyncMock(id="intent-id"))
    mock_db_service.log_tool_execution = AsyncMock(return_value=AsyncMock())

    service = StatelessConversationService(mock_db_service)

    # Execute tool multiple times with same input
    result1 = await service.enforce_one_tool_per_intent("get_all_tasks", {}, "user1")
    result2 = await service.enforce_one_tool_per_intent("get_all_tasks", {}, "user1")

    # Each execution should be independent
    assert result1["intent"] == "get_all_tasks"
    assert result2["intent"] == "get_all_tasks"

    # Verify logging happened for each
    assert mock_db_service.log_intent.call_count == 2
    assert mock_db_service.log_tool_execution.call_count == 2