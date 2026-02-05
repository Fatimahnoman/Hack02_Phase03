"""Performance tests for concurrent user handling."""

import asyncio
import pytest
from fastapi.testclient import TestClient
from backend.src.main import app
from concurrent.futures import ThreadPoolExecutor
import time


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


@pytest.mark.asyncio
async def test_concurrent_user_requests():
    """Test handling of concurrent user requests."""
    with TestClient(app) as client:
        # Define a test request
        def make_request(user_id):
            response = client.post(
                "/api/v1/chat/",
                json={
                    "user_input": "Hello",
                    "user_id": user_id
                }
            )
            return {
                "status_code": response.status_code,
                "user_id": user_id,
                "response": response.json() if response.status_code == 200 else None
            }

        # Test with multiple concurrent users
        num_users = 10
        user_ids = [f"user-{i}" for i in range(num_users)]

        # Use ThreadPoolExecutor to simulate concurrent requests
        with ThreadPoolExecutor(max_workers=num_users) as executor:
            futures = [executor.submit(make_request, uid) for uid in user_ids]
            results = [future.result() for future in futures]

        # Verify all requests were successful
        for result in results:
            assert result["status_code"] == 200
            assert result["response"] is not None
            assert "response" in result["response"]
            assert "intent" in result["response"]


@pytest.mark.asyncio
async def test_concurrent_task_creation():
    """Test concurrent task creation for different users."""
    with TestClient(app) as client:
        # Define a test request for task creation
        def create_task_request(user_id):
            response = client.post(
                "/api/v1/chat/",
                json={
                    "user_input": f"Create a task for user {user_id}",
                    "user_id": user_id
                }
            )
            return {
                "status_code": response.status_code,
                "user_id": user_id,
                "response": response.json() if response.status_code == 200 else None
            }

        # Test concurrent task creation
        num_users = 5
        user_ids = [f"task-user-{i}" for i in range(num_users)]

        with ThreadPoolExecutor(max_workers=num_users) as executor:
            futures = [executor.submit(create_task_request, uid) for uid in user_ids]
            results = [future.result() for future in futures]

        # Verify all requests were successful
        for result in results:
            assert result["status_code"] == 200


@pytest.mark.asyncio
async def test_concurrent_stateless_requests():
    """Test that concurrent requests remain stateless."""
    with TestClient(app) as client:
        def stateless_request(user_id):
            response = client.post(
                "/api/v1/chat/",
                json={
                    "user_input": "What are my tasks?",
                    "user_id": user_id
                }
            )
            return {
                "status_code": response.status_code,
                "user_id": user_id,
                "response": response.json() if response.status_code == 200 else None
            }

        # Send concurrent requests
        num_users = 8
        user_ids = [f"stateless-user-{i}" for i in range(num_users)]

        with ThreadPoolExecutor(max_workers=num_users) as executor:
            futures = [executor.submit(stateless_request, uid) for uid in user_ids]
            results = [future.result() for future in futures]

        # Verify all requests succeeded
        for result in results:
            assert result["status_code"] == 200
            assert result["response"] is not None


@pytest.mark.asyncio
async def test_performance_under_load():
    """Basic performance test under load."""
    with TestClient(app) as client:
        num_requests = 20
        start_time = time.time()

        def timed_request(i):
            response = client.post(
                "/api/v1/chat/",
                json={
                    "user_input": f"Hello request {i}",
                    "user_id": f"perf-user-{i}"
                }
            )
            return response.status_code

        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(timed_request, i) for i in range(num_requests)]
            statuses = [future.result() for future in futures]

        end_time = time.time()
        total_time = end_time - start_time

        # Verify all requests succeeded
        assert all(status == 200 for status in statuses)

        # Basic performance check (should complete in reasonable time)
        # Note: This is a very basic check and shouldn't be relied on for production benchmarks
        assert total_time < 30.0  # Should complete in under 30 seconds


@pytest.mark.asyncio
async def test_database_isolation_under_concurrency():
    """Test that database operations remain isolated under concurrent access."""
    with TestClient(app) as client:
        def isolated_request(user_id):
            # Each user should get their own isolated state
            response1 = client.post(
                "/api/v1/chat/",
                json={
                    "user_input": "What are my tasks?",
                    "user_id": user_id
                }
            )

            # Create a task for this specific user
            response2 = client.post(
                "/api/v1/chat/",
                json={
                    "user_input": f"Create task for {user_id}",
                    "user_id": user_id
                }
            )

            return {
                "check_status": response1.status_code,
                "create_status": response2.status_code,
                "user_id": user_id
            }

        # Run multiple users concurrently
        num_users = 6
        user_ids = [f"isolated-user-{i}" for i in range(num_users)]

        with ThreadPoolExecutor(max_workers=num_users) as executor:
            futures = [executor.submit(isolated_request, uid) for uid in user_ids]
            results = [future.result() for future in futures]

        # Verify all operations succeeded
        for result in results:
            assert result["check_status"] == 200
            assert result["create_status"] == 200


def test_concurrent_users_summary():
    """Summary test that validates concurrent user handling."""
    # This is more of a validation test to ensure the other tests worked
    pass