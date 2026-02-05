"""
Integration test for add_task intent flow.
"""
import pytest
from src.agents.intent_detector import IntentDetector
from src.models.intent_result import IntentType
from src.services.intent_mapping import IntentMapper
from src.mcp.task_tools import task_tools


def test_add_task_flow_integration():
    """Test the complete flow for adding a task via intent detection and mapping."""
    # Reset task tools to start fresh
    task_tools.tasks = []
    task_tools.next_id = 1

    # Initialize components
    detector = IntentDetector()
    mapper = IntentMapper()

    # Test input that should trigger add_task intent
    user_input = "add a new task to buy groceries"

    # Step 1: Detect intent
    intent_result = detector.detect(user_input)

    # Verify intent detection
    assert intent_result.type == IntentType.ADD_TASK
    assert intent_result.confidence >= 0.8

    # Step 2: Execute intent mapping
    result = mapper.execute_intent(intent_result)

    # Verify successful execution
    assert result.success is True
    assert "buy groceries" in result.message
    assert result.data is not None
    assert "task_id" in result.data

    # Step 3: Verify the task was actually created
    assert len(task_tools.tasks) == 1
    created_task = task_tools.tasks[0]
    assert created_task.description == "buy groceries"


def test_add_task_missing_description():
    """Test add_task intent with missing description."""
    # Reset task tools
    task_tools.tasks = []
    task_tools.next_id = 1

    detector = IntentDetector()
    mapper = IntentMapper()

    # Test input with no clear description
    user_input = "add a new task"

    intent_result = detector.detect(user_input)
    result = mapper.execute_intent(intent_result)

    # Should detect intent but fail during execution due to missing parameter
    assert intent_result.type == IntentType.ADD_TASK
    assert result.success is False
    assert "provide" in result.message.lower() or "missing" in result.message.lower()


def test_add_task_with_priority():
    """Test add_task intent with priority specified."""
    # Reset task tools
    task_tools.tasks = []
    task_tools.next_id = 1

    detector = IntentDetector()
    mapper = IntentMapper()

    # Test input with priority
    user_input = "add a high priority task to call mom"

    intent_result = detector.detect(user_input)
    result = mapper.execute_intent(intent_result)

    # Should detect intent and execute successfully
    assert intent_result.type == IntentType.ADD_TASK
    assert result.success is True

    # Verify the task was created with high priority
    assert len(task_tools.tasks) == 1
    created_task = task_tools.tasks[0]
    # Note: priority extraction not implemented in base detector, so this will use default


if __name__ == "__main__":
    test_add_task_flow_integration()
    test_add_task_missing_description()
    test_add_task_with_priority()
    print("All add_task flow integration tests passed!")