# Tool Contract: list_tasks

**Feature**: MCP Server and Stateless Task Tooling Layer
**Date**: 2026-01-28

## Purpose
Retrieves a list of tasks from the system with optional filtering capabilities.

## Interface Definition

### Input Schema
```json
{
  "type": "object",
  "properties": {
    "status_filter": {
      "type": "string",
      "enum": ["pending", "in-progress", "completed", "failed"],
      "description": "Filter tasks by status"
    },
    "limit": {
      "type": "integer",
      "minimum": 1,
      "maximum": 1000,
      "description": "Maximum number of tasks to return",
      "default": 100
    },
    "offset": {
      "type": "integer",
      "minimum": 0,
      "description": "Number of tasks to skip",
      "default": 0
    }
  },
  "additionalProperties": false
}
```

### Output Schema
```json
{
  "type": "object",
  "properties": {
    "success": {
      "type": "boolean",
      "description": "Indicates if the operation was successful"
    },
    "tasks": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "id": {
            "type": "string",
            "format": "uuid",
            "description": "Unique identifier of the task"
          },
          "title": {
            "type": "string",
            "description": "Title of the task"
          },
          "description": {
            "type": "string",
            "description": "Description of the task"
          },
          "status": {
            "type": "string",
            "enum": ["pending", "in-progress", "completed", "failed"],
            "description": "Current status of the task"
          },
          "created_at": {
            "type": "string",
            "format": "date-time",
            "description": "Timestamp when task was created"
          },
          "updated_at": {
            "type": "string",
            "format": "date-time",
            "description": "Timestamp when task was last updated"
          },
          "completed_at": {
            "type": "string",
            "format": "date-time",
            "description": "Timestamp when task was completed (null if not completed)",
            "nullable": true
          }
        },
        "required": ["id", "title", "status", "created_at", "updated_at"]
      }
    },
    "total_count": {
      "type": "integer",
      "description": "Total number of tasks matching the filters"
    },
    "message": {
      "type": "string",
      "description": "Human-readable message about the operation result"
    }
  },
  "required": ["success", "tasks", "total_count"],
  "additionalProperties": false
}
```

## Behavior
- Returns a list of tasks matching the optional filters
- Supports pagination via limit and offset parameters
- Returns all tasks if no filters are specified
- Orders tasks by creation date (newest first)

## Error Conditions
- Returns success=false if database operation fails
- Returns empty array if no tasks match the filters

## Example Usage

### Request (no filters)
```json
{}
```

### Request (with filters)
```json
{
  "status_filter": "pending",
  "limit": 10,
  "offset": 0
}
```

### Successful Response
```json
{
  "success": true,
  "tasks": [
    {
      "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "title": "Implement user authentication",
      "description": "Add login and registration functionality",
      "status": "pending",
      "created_at": "2023-12-01T10:00:00Z",
      "updated_at": "2023-12-01T10:00:00Z",
      "completed_at": null
    }
  ],
  "total_count": 1,
  "message": "Tasks retrieved successfully"
}
```

### Error Response
```json
{
  "success": false,
  "tasks": [],
  "total_count": 0,
  "message": "Failed to retrieve tasks from database"
}
```

## Validation Rules
- Status filter must be one of allowed values if provided
- Limit must be between 1 and 1000
- Offset must be 0 or positive
- Default limit is 100
- Default offset is 0