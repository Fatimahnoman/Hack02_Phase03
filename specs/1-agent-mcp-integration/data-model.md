# Data Model: Agent-Orchestrated Task Management via MCP Tools

**Feature**: 1-agent-mcp-integration
**Date**: 2026-01-28

## Entity Definitions

### Task
Represents a specific work item that can be created, updated, or managed through natural language commands.

**Fields**:
- id (UUID): Unique identifier for the task
- title (String): The name or title of the task
- description (Text): Detailed description of the task
- status (String): Current status (e.g., "pending", "in-progress", "completed", "cancelled")
- created_at (DateTime): Timestamp when the task was created
- updated_at (DateTime): Timestamp when the task was last updated
- completed_at (DateTime, nullable): Timestamp when the task was completed
- priority (String): Priority level (e.g., "low", "medium", "high", "urgent")

**Relationships**:
- One-to-many with ToolCall (via tool_call.entity_id and tool_call.entity_type)

**Validation Rules**:
- Title is required and must be between 1-255 characters
- Status must be one of the predefined values
- Priority must be one of the predefined values

### Conversation
Represents a sequence of messages between a user and the agent, stored in the database with timestamps and metadata.

**Fields**:
- id (UUID): Unique identifier for the conversation
- created_at (DateTime): Timestamp when the conversation started
- updated_at (DateTime): Timestamp when the conversation was last updated
- metadata (JSON): Additional conversation metadata

**Relationships**:
- One-to-many with Message (via message.conversation_id)

**Validation Rules**:
- Must have a creation timestamp
- Metadata must be valid JSON

### Message
Represents an individual message within a conversation.

**Fields**:
- id (UUID): Unique identifier for the message
- conversation_id (UUID): Foreign key to Conversation
- role (String): Role of the message sender ("user", "assistant", "system", "tool")
- content (Text): The content of the message
- timestamp (DateTime): When the message was sent
- tool_call_id (UUID, nullable): Reference to associated tool call if role is "tool"

**Relationships**:
- Many-to-one with Conversation (via conversation_id)
- One-to-zero-or-one with ToolCall (via tool_call_id)

**Validation Rules**:
- Role must be one of the predefined values
- Content is required
- conversation_id must reference an existing conversation

### ToolCall
Represents an invocation of an MCP tool with parameters and results, logged for auditing purposes.

**Fields**:
- id (UUID): Unique identifier for the tool call
- function_name (String): Name of the MCP function being called
- parameters (JSON): Parameters passed to the function
- result (JSON, nullable): Result returned by the function
- status (String): Status of the call ("success", "error", "pending")
- created_at (DateTime): Timestamp when the call was initiated
- completed_at (DateTime, nullable): Timestamp when the call completed
- entity_id (UUID, nullable): ID of the entity affected by this tool call
- entity_type (String, nullable): Type of entity affected (e.g., "Task", "Conversation")

**Relationships**:
- One-to-many with Message (via message.tool_call_id) - for tool responses
- Polymorphic relationship with Task or other entities via entity_id/entity_type

**Validation Rules**:
- function_name is required
- parameters must be valid JSON
- status must be one of the predefined values
- If result is present, it must be valid JSON

## State Transitions

### Task State Transitions
- pending → in-progress: When work begins on the task
- in-progress → completed: When work is finished successfully
- in-progress → pending: When work is paused or stopped
- pending → cancelled: When the task is abandoned
- completed → in-progress: When reopening a completed task

### ToolCall State Transitions
- pending → success: When the tool call completes successfully
- pending → error: When the tool call encounters an error

## Constraints and Business Rules

1. All task operations must be performed through MCP tools (no direct manipulation)
2. Conversation history must be preserved for context in stateless agent operations
3. Tool calls must be logged for audit and monitoring purposes
4. Task state changes must be tracked with appropriate timestamps
5. Completed tasks should not be modified except to reopen them