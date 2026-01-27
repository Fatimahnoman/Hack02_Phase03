# Tool Contract: update_task

**Feature**: MCP Server and Stateless Task Tooling Layer
**Date**: 2026-01-28

## Purpose
Updates an existing task's properties by its ID.

## Interface Definition

### Input Schema
```json
{
  "type": "object",
  "properties": {
    "task_id": {
      "type": "string",
      "format": "uuid",
      "description": "ID of the task to update"
    },
    "title": {
      "type": "string",
      "minLength": 1,
      "maxLength": 255,
      "description": "New title for the task (optional)"
    },
    "description": {
      "type": "string",
      "maxLength": 10000,
      "description": "New description for the task (optional)"
    },
    "status": {
      "type": "string",
      "enum": ["pending", "in-progress", "completed", "failed"],
      "description": "New status for the task (optional)"
    }
  },
  "required": ["task_id"],
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
    "task": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "format": "uuid",
          "description": "Unique identifier of the updated task"
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
    },
    "message": {
      "type": "string",
      "description": "Human-readable message about the operation result"
    }
  },
  "required": ["success"],
  "additionalProperties": false
}
```

## Behavior
- Updates only the fields provided in the request (partial update)
- Preserves existing values for fields not provided
- Updates the `updated_at` timestamp
- Sets `completed_at` when status changes to "completed"
- Clears `completed_at` when status changes from "completed"

## Error Conditions
- Returns success=false if task_id is invalid or not found
- Returns success=false if database operation fails
- Returns success=false if title exceeds length limits when provided

## Example Usage

### Request
```json
{
  "task_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "title": "Updated task title",
  "status": "in-progress"
}
```

### Successful Response
```json
{
  "success": true,
  "task": {
    "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "title": "Updated task title",
    "description": "Original description",
    "status": "in-progress",
    "created_at": "2023-12-01T10:00:00Z",
    "updated_at": "2023-12-01T11:00:00Z",
    "completed_at": null
  },
  "message": "Task updated successfully"
}
```

### Error Response
```json
{
  "success": false,
  "message": "Task with ID a1b2c3d4-e5f6-7890-abcd-ef1234567890 not found"
}
```

## Validation Rules
- task_id is required and must be a valid UUID
- If title is provided, it must be 1-255 characters
- If status is provided, it must be one of allowed values
- At least one of title, description, or status must be provided