# Data Model: Stateless Conversation Cycle

## Overview
This document defines the data structures and relationships required to support a stateless chatbot operation that relies on database state rather than conversation memory.

## Core Entities

### 1. User
**Description**: Represents the chatbot user with identity and preferences

**Fields**:
- id (UUID/string): Unique identifier for the user
- created_at (datetime): Timestamp of user creation
- updated_at (datetime): Timestamp of last update
- preferences (JSON): User-specific settings (language, response style, etc.)

**Validation**:
- id: Required, unique
- created_at: Auto-generated, immutable
- updated_at: Auto-updated on modification

### 2. Task
**Description**: Represents user tasks managed by the chatbot system

**Fields**:
- id (UUID/string): Unique identifier for the task
- user_id (UUID/string): Foreign key linking to User
- title (string): Task title/name
- description (text): Detailed task description
- status (enum): ['pending', 'in-progress', 'completed', 'cancelled']
- created_at (datetime): Timestamp of task creation
- updated_at (datetime): Timestamp of last update
- completed_at (datetime, nullable): Timestamp when task was completed

**Validation**:
- id: Required, unique
- user_id: Required, must reference existing User
- title: Required, length 1-255 characters
- status: Must be one of the allowed enum values
- created_at: Auto-generated, immutable
- updated_at: Auto-updated on modification

### 3. ConversationContext
**Description**: Stores necessary conversation context in the database for stateless operation

**Fields**:
- id (UUID/string): Unique identifier for the context record
- user_id (UUID/string): Foreign key linking to User
- context_type (enum): ['task-assist', 'general-chat', 'follow-up', 'custom']
- context_data (JSON): Serialized context information needed for conversation continuity
- expires_at (datetime): Expiration timestamp to prevent stale contexts
- created_at (datetime): Timestamp of context creation

**Validation**:
- id: Required, unique
- user_id: Required, must reference existing User
- context_type: Required, must be one of allowed enum values
- expires_at: Required, must be in the future

### 4. IntentLog
**Description**: Records all parsed intents for audit, debugging, and consistency verification

**Fields**:
- id (UUID/string): Unique identifier for the log entry
- user_id (UUID/string): Foreign key linking to User
- input_text (text): Original user input
- detected_intent (string): Classified intent from the input
- extracted_parameters (JSON): Parameters extracted from the input
- processed_at (datetime): Timestamp when intent was processed
- session_id (string): Identifier for the session (for grouping related requests)

**Validation**:
- id: Required, unique
- user_id: Required, must reference existing User
- input_text: Required
- detected_intent: Required
- processed_at: Auto-generated

### 5. ToolExecution
**Description**: Tracks all tool executions for validation and debugging

**Fields**:
- id (UUID/string): Unique identifier for the execution record
- intent_log_id (UUID/string): Foreign key linking to IntentLog
- tool_name (string): Name of the executed tool
- input_parameters (JSON): Parameters passed to the tool
- execution_result (JSON): Result returned by the tool
- execution_status (enum): ['success', 'failure', 'partial']
- executed_at (datetime): Timestamp of tool execution
- error_message (string, nullable): Error details if execution failed

**Validation**:
- id: Required, unique
- intent_log_id: Required, must reference existing IntentLog
- tool_name: Required
- execution_status: Required, must be one of allowed enum values
- executed_at: Auto-generated

## Relationships

### User ↔ Task
- One-to-Many: One user can have multiple tasks
- Foreign Key: Task.user_id → User.id
- Cascade: Delete tasks when user is deleted

### User ↔ ConversationContext
- One-to-Many: One user can have multiple conversation contexts
- Foreign Key: ConversationContext.user_id → User.id
- Cascade: Delete contexts when user is deleted

### User ↔ IntentLog
- One-to-Many: One user can have multiple intent logs
- Foreign Key: IntentLog.user_id → User.id
- Cascade: Delete logs when user is deleted

### IntentLog ↔ ToolExecution
- One-to-Many: One intent log can trigger multiple tool executions
- Foreign Key: ToolExecution.intent_log_id → IntentLog.id
- Cascade: Delete executions when intent log is deleted

## State Transitions

### Task Status Transitions
- 'pending' → 'in-progress': When user starts working on task
- 'in-progress' → 'completed': When user marks task as completed
- 'in-progress' → 'pending': When user needs to pause task
- 'pending' → 'cancelled': When user cancels the task
- 'completed' → 'in-progress': When user reopens completed task

### ConversationContext Expiration
- Automatically soft-deleted when expires_at is reached
- Cleanup job periodically hard-deletes expired records

## Validation Rules

### Business Logic Constraints
1. A user cannot have more than one active 'in-progress' task of the same title
2. Completed tasks cannot be transitioned back to 'pending' without explicit user action
3. Conversation contexts must be validated against current user state before use
4. Tool execution must be logged for every successful or failed execution

### Data Integrity Constraints
1. All foreign key relationships must reference existing records
2. Text fields must be sanitized to prevent injection attacks
3. Timestamps must be consistent with server time (no future dates for completion)
4. JSON fields must be valid JSON and conform to expected schema

## Indexing Strategy

### Primary Indices
- User.id (primary key)
- Task.id (primary key)
- ConversationContext.id (primary key)
- IntentLog.id (primary key)
- ToolExecution.id (primary key)

### Secondary Indices
- User.created_at (for temporal queries)
- Task.user_id (for user-specific queries)
- Task.status (for status-based queries)
- ConversationContext.user_id (for user-specific queries)
- ConversationContext.expires_at (for cleanup queries)
- IntentLog.user_id (for user-specific queries)
- IntentLog.processed_at (for temporal queries)
- ToolExecution.intent_log_id (for join queries)
- ToolExecution.tool_name (for tool-specific queries)
- ToolExecution.executed_at (for temporal queries)

## Access Patterns

### Frequent Queries
1. Get all tasks for a user filtered by status
2. Create or update a single task for a user
3. Retrieve conversation context for a user
4. Log intent and tool execution for audit
5. Verify database state consistency for a user

### Performance Considerations
1. Most queries will be user-specific, so indices on user_id are critical
2. Task status queries are common, so status index is important
3. Recent activity queries benefit from timestamp indices
4. Tool execution logging should be optimized for high-volume writes