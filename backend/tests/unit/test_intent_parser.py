"""Unit tests for intent parser service."""

import pytest
from datetime import datetime
from backend.src.services.intent_parser import IntentParser


@pytest.mark.asyncio
async def test_parse_get_pending_tasks_intent():
    """Test parsing of get pending tasks intent."""
    parser = IntentParser()

    # Test various forms of getting pending tasks
    test_inputs = [
        "what are my pending tasks?",
        "show my pending tasks",
        "list my pending tasks",
        "what pending tasks do I have?"
    ]

    for test_input in test_inputs:
        result = await parser.parse(test_input)
        assert result["intent"] == "get_pending_tasks"
        assert result["confidence"] >= 0.7  # Should have high confidence


@pytest.mark.asyncio
async def test_parse_get_all_tasks_intent():
    """Test parsing of get all tasks intent."""
    parser = IntentParser()

    test_inputs = [
        "what are my tasks?",
        "show my tasks",
        "list my tasks",
        "what tasks do I have?"
    ]

    for test_input in test_inputs:
        result = await parser.parse(test_input)
        assert result["intent"] == "get_all_tasks"
        assert result["confidence"] >= 0.7


@pytest.mark.asyncio
async def test_parse_create_task_intent():
    """Test parsing of create task intent."""
    parser = IntentParser()

    test_inputs = [
        "create task to buy groceries",
        "I need to create a task to complete project",
        "add task to call mom",
        "make a task to finish homework"
    ]

    for test_input in test_inputs:
        result = await parser.parse(test_input)
        assert result["intent"] == "create_task"
        assert result["confidence"] >= 0.7
        # Should extract parameters like title and description
        params = result["parameters"]
        assert "original_text" in params
        assert len(params["original_text"]) > 0


@pytest.mark.asyncio
async def test_parse_greeting_intent():
    """Test parsing of greeting intent."""
    parser = IntentParser()

    test_inputs = [
        "hello",
        "hi",
        "hey",
        "good morning"
    ]

    for test_input in test_inputs:
        result = await parser.parse(test_input)
        assert result["intent"] == "greeting"
        assert result["confidence"] >= 0.7


@pytest.mark.asyncio
async def test_parse_help_intent():
    """Test parsing of help intent."""
    parser = IntentParser()

    test_inputs = [
        "help",
        "what can you do",
        "how does this work"
    ]

    for test_input in test_inputs:
        result = await parser.parse(test_input)
        assert result["intent"] == "help"
        assert result["confidence"] >= 0.7


@pytest.mark.asyncio
async def test_validate_create_task_parameters():
    """Test validation of create task parameters."""
    parser = IntentParser()

    # Test valid parameters
    valid_params = {"title": "Test Task", "description": "Test Description"}
    result = await parser.validate_parameters("create_task", valid_params)
    assert result["valid"] is True
    assert len(result["errors"]) == 0

    # Test missing title
    invalid_params = {"description": "Test Description"}
    result = await parser.validate_parameters("create_task", invalid_params)
    assert result["valid"] is False
    assert len(result["errors"]) > 0
    assert "Task title is required" in result["errors"][0]

    # Test empty title
    empty_title_params = {"title": "", "description": "Test Description"}
    result = await parser.validate_parameters("create_task", empty_title_params)
    assert result["valid"] is False
    assert len(result["errors"]) > 0


@pytest.mark.asyncio
async def test_processed_without_history_flag():
    """Test that parsing is done without considering conversation history."""
    parser = IntentParser()

    result = await parser.parse("what are my tasks?")
    assert result["processed_without_history"] is True


@pytest.mark.asyncio
async def test_extract_parameters_for_create_task():
    """Test extraction of parameters for create task intent."""
    parser = IntentParser()

    test_input = "create task to buy milk and bread from the store"
    result = await parser.parse(test_input)

    if result["intent"] == "create_task":
        params = result["parameters"]
        assert "title" in params
        assert "original_text" in params
        # Should extract meaningful title from the input
        assert len(params["title"]) > 0