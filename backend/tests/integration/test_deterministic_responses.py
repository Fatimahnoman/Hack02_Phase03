"""Integration tests for deterministic response generation."""

import pytest
from fastapi.testclient import TestClient
from backend.src.main import app
from backend.src.services.stateless_conversation_service import StatelessConversationService
from backend.src.services.database_service import DatabaseService
from backend.src.services.intent_parser import IntentParser
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime
import hashlib


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


def calculate_response_hash(response_data):
    """Calculate a hash of the response data for comparison."""
    # Convert the response to a string representation
    response_str = str(sorted(response_data.items())) if isinstance(response_data, dict) else str(response_data)
    return hashlib.sha256(response_str.encode()).hexdigest()


@pytest.mark.asyncio
async def test_identical_inputs_produce_identical_outputs():
    """Test that identical inputs under same database conditions produce identical outputs."""
    with TestClient(app) as client:
        user_id = "test-deterministic-user"

        # Send the same request multiple times
        request_payload = {
            "user_input": "What are my pending tasks?",
            "user_id": user_id
        }

        responses = []
        hashes = []

        for i in range(5):  # Test multiple times
            response = client.post("/api/v1/chat/", json=request_payload)
            assert response.status_code == 200

            data = response.json()
            responses.append(data)
            hashes.append(calculate_response_hash(data))

        # All hashes should be identical
        first_hash = hashes[0]
        for i, h in enumerate(hashes[1:], 1):
            assert h == first_hash, f"Response {i+1} differs from the first response"


@pytest.mark.asyncio
async def test_same_user_same_input_deterministic():
    """Test that same user with same input always produces same output."""
    with TestClient(app) as client:
        user_id = "test-same-user-input"

        inputs_to_test = [
            "Hello",
            "What are my tasks?",
            "Create a task to water plants",
            "Show all tasks"
        ]

        for test_input in inputs_to_test:
            request_payload = {
                "user_input": test_input,
                "user_id": user_id
            }

            # Send the same request twice
            response1 = client.post("/api/v1/chat/", json=request_payload)
            response2 = client.post("/api/v1/chat/", json=request_payload)

            assert response1.status_code == 200
            assert response2.status_code == 200

            data1 = response1.json()
            data2 = response2.json()

            # Both responses should be identical
            assert data1["intent"] == data2["intent"]
            # Note: We don't compare the full response because timestamps will differ


@pytest.mark.asyncio
async def test_different_users_same_input():
    """Test that different users with same input get equivalent responses."""
    with TestClient(app) as client:
        inputs_to_test = [
            "Hello",
            "What are my tasks?"
        ]

        for test_input in inputs_to_test:
            # Different user IDs with same input
            response1 = client.post("/api/v1/chat/", json={
                "user_input": test_input,
                "user_id": "user1"
            })

            response2 = client.post("/api/v1/chat/", json={
                "user_input": test_input,
                "user_id": "user2"
            })

            assert response1.status_code == 200
            assert response2.status_code == 200

            data1 = response1.json()
            data2 = response2.json()

            # The intents should be the same for the same input
            assert data1["intent"] == data2["intent"]


@pytest.mark.asyncio
async def test_intent_parser_deterministic():
    """Test that the intent parser produces deterministic results."""
    parser = IntentParser()

    test_inputs = [
        "Hello",
        "What are my tasks?",
        "Create a task to buy groceries",
        "Show me pending tasks"
    ]

    for test_input in test_inputs:
        # Parse the same input multiple times
        results = []
        for i in range(3):
            result = await parser.parse(test_input)
            results.append(result)

        # All results should be identical
        first_result = results[0]
        for i, result in enumerate(results[1:], 1):
            assert result["intent"] == first_result["intent"], f"Mismatch for input '{test_input}' at attempt {i+1}"
            assert result["confidence"] == first_result["confidence"], f"Confidence mismatch for input '{test_input}' at attempt {i+1}"


@pytest.mark.asyncio
async def test_response_hash_consistency():
    """Test that responses can be consistently hashed for verification."""
    with TestClient(app) as client:
        request_payload = {
            "user_input": "What are my tasks?",
            "user_id": "hash-test-user"
        }

        response = client.post("/api/v1/chat/", json=request_payload)
        assert response.status_code == 200

        data = response.json()

        # Calculate hash multiple times to ensure consistency
        hash1 = calculate_response_hash(data)
        hash2 = calculate_response_hash(data)

        assert hash1 == hash2, "Response hashing is not consistent"


@pytest.mark.asyncio
async def test_stateless_conversation_service_deterministic():
    """Test that the stateless conversation service generates deterministic responses."""
    # Mock database service
    mock_session = AsyncMock()
    mock_db_service = DatabaseService(mock_session)

    # Mock the database methods with consistent returns
    mock_db_service.get_user_state_summary = AsyncMock(return_value={
        "user_id": "test-user",
        "task_count": 0,
        "task_counts_by_status": {},
        "recent_intents_count": 0
    })
    mock_db_service.get_user_tasks = AsyncMock(return_value=[])
    mock_db_service.log_intent = AsyncMock(return_value=AsyncMock(id="intent-log-id"))
    mock_db_service.log_tool_execution = AsyncMock(return_value=AsyncMock())

    service = StatelessConversationService(mock_db_service)

    # Process the same request multiple times
    test_input = "What are my tasks?"
    user_id = "service-test-user"

    results = []
    for i in range(3):
        result = await service.process_request(
            user_input=test_input,
            user_id=user_id
        )
        results.append(result)

    # All results should have the same intent
    first_intent = results[0]["intent"]
    for i, result in enumerate(results[1:], 1):
        assert result["intent"] == first_intent, f"Intent mismatch at attempt {i+1}"


@pytest.mark.asyncio
async def test_tool_execution_deterministic():
    """Test that tool execution is deterministic."""
    mock_session = AsyncMock()
    mock_db_service = DatabaseService(mock_session)

    # Set up consistent mocks
    mock_db_service.get_user_state_summary = AsyncMock(return_value={
        "user_id": "test-user",
        "task_count": 2,
        "task_counts_by_status": {"pending": 1, "completed": 1},
        "recent_intents_count": 0
    })
    mock_db_service.get_user_tasks = AsyncMock(return_value=[
        MagicMock(title="Task 1", status="pending"),
        MagicMock(title="Task 2", status="completed")
    ])
    mock_db_service.log_intent = AsyncMock(return_value=AsyncMock(id="intent-log-id"))
    mock_db_service.log_tool_execution = AsyncMock(return_value=AsyncMock())

    service = StatelessConversationService(mock_db_service)

    # Execute the same tool multiple times
    results = []
    for i in range(3):
        tool_result = await service._execute_get_all_tasks_tool("test-user")
        results.append(tool_result)

    # All results should be the same
    first_result = results[0]
    for i, result in enumerate(results[1:], 1):
        assert result["success"] == first_result["success"]
        assert result["execution_result"]["task_count"] == first_result["execution_result"]["task_count"]


@pytest.mark.asyncio
async def test_response_generation_consistency():
    """Test that response generation from tool output is consistent."""
    mock_session = AsyncMock()
    mock_db_service = DatabaseService(mock_session)

    # Mock the state summary consistently
    consistent_state = {
        "user_id": "test-user",
        "task_count": 1,
        "task_counts_by_status": {"pending": 1},
        "recent_intents_count": 0
    }
    mock_db_service.get_user_state_summary = AsyncMock(return_value=consistent_state)

    service = StatelessConversationService(mock_db_service)

    # Test that the same tool result generates the same response
    tool_result = {
        "response": "You have 1 tasks total: Task 1 (pending)",
        "execution_result": {"task_count": 1, "tasks": [{"title": "Task 1", "status": "pending"}]},
        "success": True
    }

    # Generate response multiple times
    responses = []
    for i in range(3):
        response = await service.implement_response_generation_from_tool_output(tool_result, consistent_state)
        responses.append(response)

    # All responses should be identical
    first_response = responses[0]
    for i, response in enumerate(responses[1:], 1):
        assert response == first_response, f"Response generation is not deterministic: {i+1}"


@pytest.mark.asyncio
async def test_validation_results_consistency():
    """Test that validation results are consistent."""
    mock_session = AsyncMock()
    mock_db_service = DatabaseService(mock_session)

    service = StatelessConversationService(mock_db_service)

    # Test validation with the same input multiple times
    test_result = {
        "response": "Test response",
        "execution_result": {"test": "value"},
        "success": True
    }

    validation_results = []
    for i in range(3):
        validation = await service.implement_success_failure_validation(test_result)
        validation_results.append(validation)

    # All validation results should be identical
    first_validation = validation_results[0]
    for i, validation in enumerate(validation_results[1:], 1):
        assert validation["success"] == first_validation["success"]
        assert validation["is_valid"] == first_validation["is_valid"]


@pytest.mark.asyncio
async def test_identical_inputs_detection():
    """Test that the system can detect identical inputs."""
    mock_session = AsyncMock()
    mock_db_service = DatabaseService(mock_session)

    # Mock get_user_intents to return some historical data
    mock_intent = MagicMock()
    mock_intent.input_text = "What are my tasks?"
    mock_intent.processed_at = datetime.utcnow()
    mock_intent.detected_intent = "get_all_tasks"

    mock_db_service.get_user_intents = AsyncMock(return_value=[mock_intent])
    service = StatelessConversationService(mock_db_service)

    # Check for identical inputs
    identical_results = await service.check_identical_inputs(
        user_id="test-user",
        current_input="What are my tasks?"
    )

    # Should find the identical input
    assert len(identical_results) > 0
    assert identical_results[0]["input"] == "What are my tasks?"

    # Check with a different input
    different_results = await service.check_identical_inputs(
        user_id="test-user",
        current_input="Different input"
    )

    # Should find no identical inputs
    assert len(different_results) == 0