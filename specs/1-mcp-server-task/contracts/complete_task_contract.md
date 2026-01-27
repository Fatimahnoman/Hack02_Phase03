# Tool Contract: complete_task

**Feature**: MCP Server and Stateless Task Tooling Layer
**Date**: 2026-01-28

## Purpose
Marks a task as completed by its ID.

## Interface Definition

### Input Schema
```json
{
  "type": "object",
  "properties": {
    "task_id": {
      "type": "string",
      "format": "uuid",
      "description": "ID of the task to mark as completed"
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
          "description": "Unique identifier of the completed task"
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
          "description": "Timestamp when task was completed",
          "nullable": true
        }
      },
      "required": ["id", "title", "status", "created_at", "updated_at", "completed_at"]
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
- Changes the task status to "completed"
- Sets the `completed_at` timestamp to current time
- Updates the `updated_at` timestamp
- Returns the updated task object

## Error Conditions
- Returns success=false if task_id is invalid or not found
- Returns success=false if database operation fails
- Returns success=false if task is already completed

## Example Usage

### Request
```json
{
  "task_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
}
```

### Successful Response
```json
{
  "success": true,
  "task": {
    "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "title": "Implement user authentication",
    "description": "Add login and registration functionality",
    "status": "completed",
    "created_at": "2023-12-01T10:00:00Z",
    "updated_at": "2023-12-01T12:00:00Z",
    "completed_at": "2023-12-01T12:00:00Z"
  },
  "message": "Task marked as completed successfully"
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
- Task must exist and not already be completed
- Task status cannot transition from "completed" to another status without explicit update_task call