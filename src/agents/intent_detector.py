"""
Intent Detector module for detecting user intents from natural language input.
"""
import re
from typing import Dict, List, Optional, Tuple
from ..models.intent_result import IntentType, IntentParameter, IntentResult


from ..models.intent_result import IntentResult, IntentParameter


class IntentDetector:
    """Base class for intent detection functionality."""

    def __init__(self):
        self.keyword_patterns = {
            IntentType.ADD_TASK: [
                r'\b(add|create|make|new)\s+(a\s+)?task\b',
                r'\b(task|todo)\s+(to|for)\s+',
                r'\bneed\s+to\s+',
                r'\bhave\s+to\s+',
                r'\bgotta\s+',
                r'\bmust\s+'
            ],
            IntentType.LIST_TASKS: [
                r'\b(list|show|display|view|get|fetch)\s+(me\s+)?(my\s+)?(tasks|todos|to-dos)\b',
                r'\b(list|show|display|view|get|fetch)\s+(me\s+)?(my\s+)?(completed|pending|active|open|closed)\s+(tasks|todos|to-dos)\b',
                r'\bwhat.*tasks?\b',
                r'\bsaved\s+todays?\b',
                r'\bremind\s+me\s+about\s+tasks?\b'
            ],
            IntentType.UPDATE_TASK: [
                r'\b(update|change|modify|edit)\s+(task|todo)\b',
                r'\b(change|modify|update).*\b(task|todo)\b'
            ],
            IntentType.COMPLETE_TASK: [
                r'\b(complete|finish|done|accomplish|check|mark.*done)\s+(task|todo)\b',
                r'\b(mark|set)\s+(as\s+)?(complete|done)\b'
            ],
            IntentType.DELETE_TASK: [
                r'\b(delete|remove|kill|erase)\s+(task|todo)\b',
                r'\b(get\s+rid\s+of|trash)\s+(task|todo)\b'
            ],
            IntentType.HELP: [
                r'\b(help|support|assistance|how\s+do|what\s+can|commands?)\b',
                r'\bwhat.*can.*do\b',
                r'\bhow.*work\b'
            ]
        }

    def detect(self, input_text: str) -> IntentResult:
        """
        Detect intent from input text.

        Args:
            input_text: The user's input text

        Returns:
            IntentResult containing the detected intent and parameters
        """
        if not input_text.strip():
            return IntentResult(IntentType.UNKNOWN, confidence=0.0)

        # Normalize the input
        normalized_input = input_text.lower().strip()

        # Check for each intent type
        for intent_type, patterns in self.keyword_patterns.items():
            for pattern in patterns:
                if re.search(pattern, normalized_input):
                    # Extract parameters based on intent type
                    parameters = self._extract_parameters(intent_type, normalized_input)

                    # Determine required parameters for the intent
                    required_params = self._get_required_parameters(intent_type)

                    return IntentResult(
                        intent_type=intent_type,
                        confidence=0.9 if len(patterns) > 0 else 0.5,
                        parameters=parameters,
                        required_parameters=required_params
                    )

        # If no specific intent matched, return unknown
        return IntentResult(IntentType.UNKNOWN, confidence=0.1)

    def _extract_parameters(self, intent_type: IntentType, input_text: str) -> IntentParameter:
        """Extract parameters from input text based on intent type."""
        params = {}

        if intent_type == IntentType.ADD_TASK:
            # Extract task description
            # Look for text after common task starters
            for pattern in [r'\b(to|for)\s+(.+)', r'\b(need\s+to|have\s+to|gotta|must)\s+(.+)']:
                match = re.search(pattern, input_text)
                if match:
                    task_desc = match.group(1) if len(match.groups()) == 1 else match.group(2)
                    # Clean up the description
                    task_desc = re.sub(r'(please|now|today|tomorrow)', '', task_desc).strip()
                    if task_desc:
                        params['task_description'] = task_desc
                    break

        elif intent_type == IntentType.UPDATE_TASK:
            # Extract task ID if mentioned
            id_match = re.search(r'\b(\d+)\b', input_text)
            if id_match:
                params['task_id'] = int(id_match.group(1))

        elif intent_type == IntentType.COMPLETE_TASK or intent_type == IntentType.DELETE_TASK:
            # Extract task ID if mentioned
            id_match = re.search(r'\b(\d+)\b', input_text)
            if id_match:
                params['task_id'] = int(id_match.group(1))

        elif intent_type == IntentType.LIST_TASKS:
            # Check if filtered by status
            if re.search(r'(completed|done|finished)', input_text):
                params['status'] = 'completed'
            elif re.search(r'(pending|active|incomplete)', input_text):
                params['status'] = 'pending'

        return IntentParameter(**params)

    def _get_required_parameters(self, intent_type: IntentType) -> List[str]:
        """Get list of required parameters for an intent type."""
        required = {
            IntentType.ADD_TASK: ['task_description'],
            IntentType.UPDATE_TASK: ['task_id'],
            IntentType.COMPLETE_TASK: ['task_id'],
            IntentType.DELETE_TASK: ['task_id']
        }
        return required.get(intent_type, [])