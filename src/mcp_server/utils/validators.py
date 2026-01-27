from typing import Dict, Any, Optional
from src.mcp_server.models.task import TaskStatus
import uuid


def validate_task_title(title: str) -> tuple[bool, Optional[str]]:
    """
    Validate task title.

    Args:
        title: The title to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not title or not title.strip():
        return False, "Title is required and cannot be empty"

    if len(title.strip()) < 1:
        return False, "Title must be at least 1 character long"

    if len(title) > 255:
        return False, "Title must be no more than 255 characters"

    return True, None


def validate_task_description(description: Optional[str]) -> tuple[bool, Optional[str]]:
    """
    Validate task description.

    Args:
        description: The description to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if description and len(description) > 10000:
        return False, "Description must be no more than 10,000 characters"

    return True, None


def validate_task_status(status: str) -> tuple[bool, Optional[str]]:
    """
    Validate task status.

    Args:
        status: The status to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        TaskStatus(status)
        return True, None
    except ValueError:
        return False, f"Invalid status. Must be one of: {', '.join([s.value for s in TaskStatus])}"


def validate_task_id(task_id: str) -> tuple[bool, Optional[str]]:
    """
    Validate task ID is a valid UUID.

    Args:
        task_id: The task ID to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        uuid.UUID(task_id)
        return True, None
    except ValueError:
        return False, "Invalid task ID format. Must be a valid UUID"


def validate_pagination_params(limit: int, offset: int) -> tuple[bool, Optional[str]]:
    """
    Validate pagination parameters.

    Args:
        limit: The limit parameter
        offset: The offset parameter

    Returns:
        Tuple of (is_valid, error_message)
    """
    if limit < 1 or limit > 1000:
        return False, "Limit must be between 1 and 1000"

    if offset < 0:
        return False, "Offset must be 0 or greater"

    return True, None