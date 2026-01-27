# Tool Contract: add_task

**Feature**: MCP Server and Stateless Task Tooling Layer
**Date**: 2026-01-28

## Purpose
Creates a new task in the system with the provided title and description.

## Interface Definition

### Input Schema
```json
{
  "type": "object",
  "properties": {
    "title": {
      "type": "string",
      "minLength": 1,
      "maxLength": 255,
      "description": "Brief title of the task"
    },
    "description": {
      "type": "string",
      "maxLength": 10000,
      "description": "Detailed description of the task",
      "default": ""
    }
  },
  "required": ["title"],
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
          "description": "Unique identifier of the created task"
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
        }
      },
      "required": ["id", "title", "status", "created_at", "updated_at"]
    },
    "message": {
      "type": "string",
      "description": "Human-readable message about the operation result"
    }
  },
  "required": ["success", "task"],
  "additionalProperties": false
}
```

## Behavior
- Creates a new task with the provided title and description
- Sets the initial status to "pending"
- Generates a unique ID for the task
- Sets creation and update timestamps
- Returns the created task object

## Error Conditions
- Returns success=false if title is missing or empty
- Returns success=false if database operation fails
- Returns success=false if title exceeds length limits

## Example Usage

### Request
```json
{
  "title": "Implement user authentication",
  "description": "Add login and registration functionality"
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
    "status": "pending",
    "created_at": "2023-12-01T10:00:00Z",
    "updated_at": "2023-12-01T10:00:00Z"
  },
  "message": "Task created successfully"
}
```

### Error Response
```json
{
  "success": false,
  "message": "Title is required and cannot be empty"
}
```

## Validation Rules
- Title must be 1-255 characters
- Description is optional, max 10,000 characters
- Status defaults to "pending"
- ID is auto-generated as UUID