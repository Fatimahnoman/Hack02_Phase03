"""Intent parser service for the stateless chatbot."""

import re
from typing import Dict, Any, Optional
import json
from datetime import datetime


class IntentParser:
    """Service to parse user input and determine intent without relying on conversation history."""

    def __init__(self):
        # Define intent patterns for the stateless chatbot
        self.intent_patterns = {
            "get_pending_tasks": [
                r"(what are my|show my|list my|display my|view my).*pending.*tasks?",
                r"(what are my|show my|list my|display my|view my).*tasks?.*pending",
                r"pending.*tasks?",
                r"tasks?.*pending",
                r"what.*pending",
                r"show.*pending",
                r"list.*pending"
            ],
            "get_all_tasks": [
                r"(what are my|show my|list my|display my|view my).*tasks?",
                r"all.*tasks?",
                r"list.*tasks?",
                r"show.*tasks?",
                r"view.*tasks?",
                r"display.*tasks?"
            ],
            "create_task": [
                r"(create|make|add|new|start).*task.*to.*",
                r"task.*to.*",
                r"need to.*",
                r"want to.*",
                r"please.*",
                r"create.*",
                r"make.*"
            ],
            "get_completed_tasks": [
                r"(what are my|show my|list my|display my|view my).*completed.*tasks?",
                r"(what are my|show my|list my|display my|view my).*tasks?.*completed",
                r"completed.*tasks?",
                r"tasks?.*completed",
                r"done.*tasks?",
                r"finished.*tasks?"
            ],
            "update_task": [
                r"(update|change|modify|edit).*task",
                r"(update|change|modify|edit).*to.*",
                r"set.*to.*",
                r"mark.*as.*"
            ],
            "delete_task": [
                r"(delete|remove|cancel|eliminate).*task",
                r"remove.*task",
                r"delete.*task",
                r"cancel.*task"
            ],
            "greeting": [
                r"hello",
                r"hi",
                r"hey",
                r"greetings",
                r"good morning",
                r"good afternoon",
                r"good evening"
            ],
            "help": [
                r"help",
                r"assist",
                r"what can you do",
                r"how.*work",
                r"what.*do"
            ]
        }

    async def parse(self, text: str) -> Dict[str, Any]:
        """
        Parse user input to determine intent without considering past conversation history.

        Args:
            text: The input text to analyze for intent

        Returns:
            Dictionary containing the detected intent, confidence, parameters, and processing details
        """
        # Normalize input
        normalized_text = text.lower().strip()

        # Find the best matching intent
        best_match = None
        best_confidence = 0.0

        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, normalized_text):
                    # Calculate confidence based on pattern match strength
                    confidence = self._calculate_confidence(pattern, normalized_text)

                    if confidence > best_confidence:
                        best_confidence = confidence
                        best_match = intent

        # If no intent matched, classify as general
        if best_match is None:
            best_match = "general"
            best_confidence = 0.1  # Low confidence for unmatched input

        # Extract parameters based on the detected intent
        parameters = await self._extract_parameters(text, best_match)

        # Create the response
        result = {
            "intent": best_match,
            "confidence": round(best_confidence, 2),
            "parameters": parameters,
            "processed_without_history": True,
            "details": {
                "alternatives": [],  # We could add alternative intents here if needed
                "timestamp": datetime.utcnow().isoformat()
            }
        }

        return result

    def _calculate_confidence(self, pattern: str, text: str) -> float:
        """
        Calculate confidence score for a pattern match.

        Args:
            pattern: The regex pattern that matched
            text: The input text

        Returns:
            Confidence score between 0 and 1
        """
        # Simple heuristic: longer, more specific matches get higher confidence
        if re.fullmatch(pattern, text.strip(), re.IGNORECASE):
            return 1.0  # Perfect match
        elif re.match(pattern, text.strip(), re.IGNORECASE):
            return 0.9  # Direct match from start
        elif re.search(pattern, text.strip(), re.IGNORECASE):
            return 0.7  # Contains match
        else:
            return 0.0  # No match

    async def _extract_parameters(self, text: str, intent: str) -> Dict[str, Any]:
        """
        Extract parameters from the input text based on the detected intent.

        Args:
            text: The original input text
            intent: The detected intent

        Returns:
            Dictionary containing extracted parameters
        """
        parameters = {}
        text_lower = text.lower().strip()

        if intent == "create_task":
            # Look for task title and description in the text
            # Pattern: "create task to [title]" or "need to [title]"
            create_patterns = [
                r"create task to (.+?)(?:\s|$)",
                r"create.*task.*to (.+?)(?:\s|$)",
                r"need to (.+?)(?:\s|$)",
                r"want to (.+?)(?:\s|$)",
                r"add task to (.+?)(?:\s|$)"
            ]

            for pattern in create_patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    task_description = match.group(1).strip()
                    # Split potential title and description if possible
                    parts = task_description.split('.', 1)
                    parameters['title'] = parts[0].strip()
                    if len(parts) > 1:
                        parameters['description'] = parts[1].strip()
                    else:
                        parameters['description'] = task_description
                    break

            # If no specific match, use the entire text after common verbs
            if not parameters.get('title'):
                # Extract after common verbs
                for verb in ['need to', 'want to', 'please', 'create', 'make', 'add']:
                    if verb in text_lower:
                        start_idx = text_lower.find(verb) + len(verb)
                        extracted = text[start_idx:].strip()
                        if extracted:
                            parameters['title'] = extracted.split('.')[0].strip()
                            parameters['description'] = extracted
                        break

        elif intent == "update_task":
            # Look for update patterns like "update task 'title' to 'new_value'"
            update_patterns = [
                r"update.*task.*(?:'|\"|”|“)?([^'\"]+?)(?:'|\"|”|“)?\s*(?:to|with|as)\s*(?:'|\"|”|“)?([^'\"]+?)(?:'|\"|”|“)?(?:\s|$|\.)",
                r"change.*task.*(?:'|\"|”|“)?([^'\"]+?)(?:'|\"|”|“)?\s*(?:to|with|as)\s*(?:'|\"|”|“)?([^'\"]+?)(?:'|\"|”|“)?(?:\s|$|\.)",
                r"mark.*(?:'|\"|”|“)?([^'\"]+?)(?:'|\"|”|“)?\s*as\s*(?:'|\"|”|“)?([^'\"]+?)(?:'|\"|”|“)?(?:\s|$|\.)"
            ]

            for pattern in update_patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    parameters['target'] = match.group(1).strip()
                    parameters['value'] = match.group(2).strip()
                    break

        elif intent == "delete_task":
            # Look for delete patterns
            delete_patterns = [
                r"delete.*(?:'|\"|”|“)?([^'\"]+?)(?:'|\"|”|“)?",
                r"remove.*(?:'|\"|”|“)?([^'\"]+?)(?:'|\"|”|“)?",
                r"cancel.*(?:'|\"|”|“)?([^'\"]+?)(?:'|\"|”|“)?"
            ]

            for pattern in delete_patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    parameters['target'] = match.group(1).strip()
                    break

        # Always add the original text as a parameter
        parameters['original_text'] = text.strip()

        return parameters

    async def validate_parameters(self, intent: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate the extracted parameters against requirements for the intent.

        Args:
            intent: The detected intent
            parameters: Parameters to validate

        Returns:
            Dictionary containing validation result and corrected parameters
        """
        valid = True
        errors = []
        corrected_parameters = parameters.copy()

        if intent == "create_task":
            # Validate required fields for task creation
            if not parameters.get('title') or len(parameters.get('title', '').strip()) == 0:
                valid = False
                errors.append("Task title is required")

            if not parameters.get('description') or len(parameters.get('description', '').strip()) == 0:
                # Use title as description if none provided
                corrected_parameters['description'] = parameters.get('title', '')

        elif intent == "update_task":
            # Validate required fields for task update
            if not parameters.get('target'):
                valid = False
                errors.append("Target for update is required")

        elif intent == "delete_task":
            # Validate required fields for task deletion
            if not parameters.get('target'):
                valid = False
                errors.append("Target for deletion is required")

        return {
            "valid": valid,
            "errors": errors,
            "corrected_parameters": corrected_parameters
        }


async def parse_intent(text: str, user_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Standalone function to parse intent from user input.

    Args:
        text: The user input text to analyze
        user_id: Optional user ID (for context, but not used in stateless processing)

    Returns:
        Dictionary containing the parsed intent and related information
    """
    parser = IntentParser()
    result = await parser.parse(text)

    # Log the intent for audit purposes (would be saved to database in real implementation)
    intent_log = {
        "input_text": text,
        "detected_intent": result["intent"],
        "extracted_parameters": json.dumps(result["parameters"]),
        "processed_at": datetime.utcnow().isoformat(),
        "user_id": user_id
    }

    return {
        "parsed_intent": result,
        "intent_log": intent_log
    }