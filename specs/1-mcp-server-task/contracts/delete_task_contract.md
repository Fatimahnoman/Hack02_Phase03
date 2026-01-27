# Tool Contract: delete_task

**Feature**: MCP Server and Stateless Task Tooling Layer
**Date**: 2026-01-28

## Purpose
Deletes a task from the system by its ID.

## Interface Definition

### Input Schema
```json
{
  "type": "object",
  "properties": {
    "task_id": {
      "type": "string",
      "format": "uuid",
      "description": "ID of the task to delete"
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
    "message": {
      "type": "string",
      "description": "Human-readable message about the operation result"
    }
  },
  "required": ["success", "message"],
  "additionalProperties": false
}
```

## Behavior
- Permanently removes the task from the database
- Returns success response indicating operation completion
- Does not return the deleted task object

## Error Conditions
- Returns success=false if task_id is invalid or not found
- Returns success=false if database operation fails

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
  "message": "Task deleted successfully"
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
- Task must exist in the database
- Deletion is permanent and cannot be undone