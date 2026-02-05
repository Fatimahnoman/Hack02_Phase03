"""
Integration test for list_tasks intent flow.
"""
import pytest
from src.agents.intent_detector import IntentDetector
from src.models.intent_result import IntentType
from src.services.intent_mapping import IntentMapper
from src.mcp.task_tools import task_tools


def test_list_tasks_flow_integration():
    """Test the complete flow for listing tasks via intent detection and mapping."""
    # Reset task tools to start fresh and add some tasks
    task_tools.tasks = []
    task_tools.next_id = 1

    # Add some test tasks
    task_tools.create_task("Buy groceries")
    task_tools.create_task("Walk the dog", priority="high")
    task_tools.create_task("Finish report", priority="normal")

    # Initialize components
    detector = IntentDetector()
    mapper = IntentMapper()

    # Test input that should trigger list_tasks intent
    user_input = "show me my tasks"

    # Step 1: Detect intent
    intent_result = detector.detect(user_input)

    # Verify intent detection
    assert intent_result.type == IntentType.LIST_TASKS
    assert intent_result.confidence >= 0.8

    # Step 2: Execute intent mapping
    result = mapper.execute_intent(intent_result)

    # Verify successful execution
    assert result.success is True
    assert "task" in result.message.lower()
    assert result.data is not None
    assert "tasks" in result.data
    assert len(result.data["tasks"]) == 3  # Should have 3 tasks


def test_list_completed_tasks():
    """Test list_tasks intent with completed filter."""
    # Reset and setup
    task_tools.tasks = []
    task_tools.next_id = 1

    # Add some tasks
    task_tools.create_task("Buy groceries")
    result = task_tools.create_task("Complete assignment")
    task_id = result.data["task"]["id"]

    # Complete one task
    task_tools.complete_task(task_id)

    detector = IntentDetector()
    mapper = IntentMapper()

    # Test input to list completed tasks
    user_input = "show me my completed tasks"

    intent_result = detector.detect(user_input)
    result = mapper.execute_intent(intent_result)

    # Should detect as LIST_TASKS and filter by completed status
    assert intent_result.type == IntentType.LIST_TASKS
    assert result.success is True


def test_empty_tasks_list():
    """Test list_tasks intent when no tasks exist."""
    # Reset task tools
    task_tools.tasks = []
    task_tools.next_id = 1

    detector = IntentDetector()
    mapper = IntentMapper()

    user_input = "list my tasks"

    intent_result = detector.detect(user_input)
    result = mapper.execute_intent(intent_result)

    # Should return success with empty list
    assert intent_result.type == IntentType.LIST_TASKS
    assert result.success is True
    assert "0" in result.message or "found" in result.message.lower()


if __name__ == "__main__":
    test_list_tasks_flow_integration()
    test_list_completed_tasks()
    test_empty_tasks_list()
    print("All list_tasks flow integration tests passed!")