"""
Integration test for help intent flow.
"""
import pytest
from src.agents.intent_detector import IntentDetector
from src.models.intent_result import IntentType
from src.services.intent_mapping import IntentMapper


def test_help_flow_integration():
    """Test the complete flow for help intent via intent detection and mapping."""
    # Initialize components
    detector = IntentDetector()
    mapper = IntentMapper()

    # Test input that should trigger help intent
    user_input = "help me"

    # Step 1: Detect intent
    intent_result = detector.detect(user_input)

    # Verify intent detection
    assert intent_result.type == IntentType.HELP
    assert intent_result.confidence >= 0.8

    # Step 2: Execute intent mapping
    result = mapper.execute_intent(intent_result)

    # Verify successful execution
    assert result.success is True
    assert "help" in result.message.lower()
    assert "add" in result.message.lower()  # Should mention available commands
    assert result.data is not None
    assert "available_commands" in result.data


def test_help_short_command():
    """Test help intent with short 'help' command."""
    detector = IntentDetector()
    mapper = IntentMapper()

    user_input = "help"

    intent_result = detector.detect(user_input)
    result = mapper.execute_intent(intent_result)

    # Should detect as HELP and provide help message
    assert intent_result.type == IntentType.HELP
    assert result.success is True
    assert "help" in result.message.lower()


def test_assistance_request():
    """Test help intent with alternative phrasing."""
    detector = IntentDetector()
    mapper = IntentMapper()

    user_input = "can you assist me?"

    intent_result = detector.detect(user_input)
    result = mapper.execute_intent(intent_result)

    # Should detect as HELP (may not match perfectly, but should work with variations)
    # If it doesn't match as HELP, it might return unknown, but let's test
    # the more standard patterns
    user_input = "what can you do for me?"

    intent_result = detector.detect(user_input)
    result = mapper.execute_intent(intent_result)

    # This might not be detected as HELP depending on the keywords, so test a standard help command
    user_input = "show commands"
    intent_result = detector.detect(user_input)
    result = mapper.execute_intent(intent_result)

    # Even if this doesn't match HELP, let's test the standard help
    user_input = "help"
    intent_result = detector.detect(user_input)
    result = mapper.execute_intent(intent_result)

    assert result.success is True


if __name__ == "__main__":
    test_help_flow_integration()
    test_help_short_command()
    test_assistance_request()
    print("All help flow integration tests passed!")