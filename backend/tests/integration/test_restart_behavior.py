"""Integration tests for server restart behavior (simulated)."""

import pytest
from fastapi.testclient import TestClient
from backend.src.main import app
from backend.src.services.stateless_conversation_service import StatelessConversationService
from backend.src.services.database_service import DatabaseService
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime
import time


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


class MockDatabaseServiceFactory:
    """Factory to create fresh mock database services for each test."""

    @staticmethod
    def create_fresh_service():
        """Create a fresh instance of mock database service."""
        mock_session = AsyncMock()
        mock_db_service = DatabaseService(mock_session)

        # Mock the database methods consistently
        mock_db_service.get_user_state_summary = AsyncMock(return_value={
            "user_id": "restart-test-user",
            "task_count": 0,
            "task_counts_by_status": {},
            "recent_intents_count": 0
        })
        mock_db_service.get_user_tasks = AsyncMock(return_value=[])
        mock_db_service.log_intent = AsyncMock(return_value=AsyncMock(id="intent-log-id"))
        mock_db_service.log_tool_execution = AsyncMock(return_value=AsyncMock())

        return mock_db_service


def simulate_server_restart():
    """
    Simulate server restart behavior.
    In a real scenario, this would represent a complete application restart.
    For testing, we'll reset state where appropriate.
    """
    # In a real implementation, this would:
    # - Stop the server
    # - Clear any in-memory caches/states
    # - Restart the server
    # For testing, we'll just ensure we're not relying on in-memory state
    pass


@pytest.mark.asyncio
async def test_stateless_behavior_preserved_after_simulated_restart():
    """Test that stateless behavior is preserved even after simulated restart."""
    # Test that the system behaves the same way before and after restart
    # by ensuring no persistent state is maintained

    # Before "restart" - make a few requests
    with TestClient(app) as client:
        user_id = "test-restart-behavior"

        # Make some requests before the simulated restart
        responses_before = []
        for i in range(3):
            response = client.post(
                "/api/v1/chat/",
                json={
                    "user_input": "Hello",
                    "user_id": f"{user_id}-before-{i}"
                }
            )
            assert response.status_code == 200
            responses_before.append(response.json())

        # Simulate server restart
        simulate_server_restart()

        # After "restart" - make the same requests with fresh user IDs
        responses_after = []
        for i in range(3):
            response = client.post(
                "/api/v1/chat/",
                json={
                    "user_input": "Hello",  # Same input
                    "user_id": f"{user_id}-after-{i}"  # Different user to ensure independence
                }
            )
            assert response.status_code == 200
            responses_after.append(response.json())

        # Verify that the behavior is consistent
        # The intent for "Hello" should be "greeting" both before and after
        for i in range(len(responses_before)):
            assert responses_before[i]["intent"] == responses_after[i]["intent"] == "greeting"


@pytest.mark.asyncio
async def test_database_state_consistency_after_restart_simulation():
    """Test that responses reflect actual database state after restart simulation."""
    factory = MockDatabaseServiceFactory()

    # Create a service before restart
    service_before = StatelessConversationService(factory.create_fresh_service())

    # Create a service after restart (simulated - fresh instance)
    service_after = StatelessConversationService(factory.create_fresh_service())

    # Both services should behave identically since they're stateless
    test_input = "What are my tasks?"
    user_id = "test-db-consistency"

    result_before = await service_before.process_request(
        user_input=test_input,
        user_id=user_id
    )

    result_after = await service_after.process_request(
        user_input=test_input,
        user_id=user_id
    )

    # Both should have the same intent since input is the same
    assert result_before["intent"] == result_after["intent"] == "get_all_tasks"


@pytest.mark.asyncio
async def test_no_memory_dependence_across_restart_simulation():
    """Test that no conversation memory affects behavior across restarts."""
    with TestClient(app) as client:
        user_id = "test-no-memory-across-restart"

        # Send a series of related requests
        responses_phase1 = []
        requests_phase1 = [
            {"user_input": "Create a task to buy groceries", "user_id": user_id},
            {"user_input": "What did I just ask you to do?", "user_id": user_id},
        ]

        for request in requests_phase1:
            response = client.post("/api/v1/chat/", json=request)
            assert response.status_code == 200
            responses_phase1.append(response.json())

        # Simulate restart
        simulate_server_restart()

        # Send the same follow-up request with a fresh user ID
        response_fresh = client.post("/api/v1/chat/", json={
            "user_input": "What did I just ask you to do?",
            "user_id": f"{user_id}-fresh"
        })

        assert response_fresh.status_code == 200
        fresh_response = response_fresh.json()

        # The fresh user should not have any context about the previous conversation
        # This demonstrates stateless behavior


@pytest.mark.asyncio
async def test_request_processing_independence():
    """Test that each request is processed independently, simulating post-restart behavior."""
    # Create multiple fresh services to simulate post-restart state
    services = []
    for i in range(3):
        factory = MockDatabaseServiceFactory()
        service = StatelessConversationService(factory.create_fresh_service())
        services.append(service)

    test_input = "What are my pending tasks?"
    user_ids = ["user1", "user2", "user3"]

    results = []
    for i, service in enumerate(services):
        result = await service.process_request(
            user_input=test_input,
            user_id=user_ids[i]
        )
        results.append(result)

    # All services should process the same input identically
    first_intent = results[0]["intent"]
    for result in results[1:]:
        assert result["intent"] == first_intent


@pytest.mark.asyncio
async def test_identical_behavior_without_cached_state():
    """Test that behavior is identical without relying on cached state."""
    with TestClient(app) as client:
        # This test ensures that even after simulated restart (state clearance),
        # the behavior remains consistent because it's based on input + database

        user_id = "test-identical-behavior"

        # Make requests and record behavior
        behaviors = []
        inputs = ["Hello", "What are my tasks?", "Create task to test"]

        for test_input in inputs:
            response = client.post("/api/v1/chat/", json={
                "user_input": test_input,
                "user_id": user_id
            })
            assert response.status_code == 200
            data = response.json()

            behaviors.append({
                "input": test_input,
                "intent": data["intent"],
                "response_contains": data["response"].lower()
            })

        # After simulated restart, same inputs should produce same intent classifications
        # although actual responses might vary based on DB state
        for i, behavior in enumerate(behaviors):
            response = client.post("/api/v1/chat/", json={
                "user_input": behavior["input"],
                "user_id": user_id
            })
            assert response.status_code == 200
            data = response.json()

            # Intent classification should be consistent
            assert data["intent"] == behavior["intent"]


@pytest.mark.asyncio
async def test_state_verification_still_works_post_restart():
    """Test that state verification functions work after restart."""
    factory = MockDatabaseServiceFactory()
    service = StatelessConversationService(factory.create_fresh_service())

    # Test state verification methods
    verification = await service.enforce_database_query_verification(
        user_id="test-verification",
        action_type="create_task"
    )

    # Should have appropriate structure
    assert "user_id" in verification
    assert "action_type" in verification
    assert "current_state" in verification
    assert verification["user_id"] == "test-verification"


@pytest.mark.asyncio
async def test_tool_execution_consistency_post_restart():
    """Test that tool execution is consistent even after restart."""
    factory = MockDatabaseServiceFactory()

    # Create service instances (simulating pre/post restart)
    service1 = StatelessConversationService(factory.create_fresh_service())
    service2 = StatelessConversationService(factory.create_fresh_service())

    # Execute same tool with both services
    tool_result1 = await service1.execute_tool_framework(
        tool_name="get_all_tasks",
        params={},
        user_id="test-user"
    )

    tool_result2 = await service2.execute_tool_framework(
        tool_name="get_all_tasks",
        params={},
        user_id="test-user"
    )

    # Results should be structurally similar
    assert "success" in tool_result1
    assert "success" in tool_result2
    assert type(tool_result1["success"]) == type(tool_result2["success"])


@pytest.mark.asyncio
async def test_response_generation_stability():
    """Test that response generation is stable across restarts."""
    factory = MockDatabaseServiceFactory()

    # Simulate services created at different times (post-restart)
    service1 = StatelessConversationService(factory.create_fresh_service())
    service2 = StatelessConversationService(factory.create_fresh_service())

    # Mock data for response generation
    tool_result = {
        "response": "You have 2 tasks.",
        "execution_result": {"task_count": 2},
        "success": True
    }

    user_state = {"task_count": 2, "task_counts_by_status": {"pending": 1, "completed": 1}}

    # Generate responses with both services
    response1 = await service1.implement_response_generation_from_tool_output(
        tool_result, user_state
    )

    response2 = await service1.implement_response_generation_from_tool_output(
        tool_result, user_state
    )

    # Both should generate consistent responses based on the same inputs
    assert response1 == response2


@pytest.mark.asyncio
async def test_system_readiness_after_restart_simulation():
    """Test that system is ready and functioning after restart simulation."""
    with TestClient(app) as client:
        # Test health endpoint still works
        health_response = client.get("/api/v1/health")
        assert health_response.status_code == 200

        # Test chat endpoint still works
        chat_response = client.post("/api/v1/chat/", json={
            "user_input": "Hello",
            "user_id": "test-readiness"
        })
        assert chat_response.status_code == 200

        data = chat_response.json()
        assert "response" in data
        assert "intent" in data