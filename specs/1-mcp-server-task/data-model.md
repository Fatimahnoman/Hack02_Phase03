# Data Model: MCP Server Task Management

**Feature**: MCP Server and Stateless Task Tooling Layer
**Date**: 2026-01-28

## Entity: Task

### Attributes
- **id** (UUID/String, Primary Key)
  - Unique identifier for each task
  - Auto-generated upon creation
  - Immutable after creation

- **title** (String, Required, Max 255 chars)
  - Brief description of the task
  - Required for all tasks
  - Cannot be empty

- **description** (Text, Optional)
  - Detailed description of the task
  - May be empty or null
  - Supports rich text content

- **status** (Enum, Required)
  - Current state of the task
  - Values: "pending", "in-progress", "completed", "failed"
  - Default: "pending"

- **created_at** (DateTime, Required)
  - Timestamp when task was created
  - Auto-set on creation
  - Immutable after creation

- **updated_at** (DateTime, Required)
  - Timestamp when task was last modified
  - Auto-updated on any modification
  - Updated on every save operation

- **completed_at** (DateTime, Optional)
  - Timestamp when task was marked as completed
  - Null if task is not completed
  - Set when status changes to "completed"

### Constraints
- Title must not be empty or whitespace-only
- Status must be one of the allowed values
- created_at and updated_at are automatically managed
- completed_at is only set when status is "completed"

### Indexes
- Primary key index on id
- Index on status for efficient filtering
- Index on created_at for chronological ordering

## Relationship Diagram

```
[Task]
├── id: UUID (PK)
├── title: String (Required)
├── description: Text (Optional)
├── status: Enum (Required)
├── created_at: DateTime (Required)
├── updated_at: DateTime (Required)
└── completed_at: DateTime (Optional)
```

## Database Schema (SQLModel)

```python
from sqlmodel import SQLModel, Field, Column
from datetime import datetime
import uuid

class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None)
    status: str = Field(default="pending", sa_column=Column(sa.Enum("pending", "in-progress", "completed", "failed", name="task_status")))

class Task(TaskBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: datetime | None = Field(default=None)

class TaskRead(TaskBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    completed_at: datetime | None

class TaskCreate(TaskBase):
    title: str
    description: str | None = None

class TaskUpdate(SQLModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None
```

## Validation Rules

### Input Validation
- Title: Required, 1-255 characters, trimmed of leading/trailing whitespace
- Description: Optional, maximum 10,000 characters
- Status: Must be one of allowed enum values
- ID: Auto-generated, not accepted as input

### Business Logic Validation
- Status transitions: Only certain transitions are allowed (e.g., pending → in-progress, in-progress → completed/failed)
- Completed tasks cannot be modified except to change status back to in-progress
- completed_at is automatically set when status becomes "completed"
- updated_at is automatically updated on any change

## API Schema Objects

### Request Schemas
- `TaskCreateRequest`: Contains title and description (status defaults to "pending")
- `TaskUpdateRequest`: Contains optional fields for partial updates
- `TaskCompleteRequest`: Contains optional completion notes

### Response Schemas
- `TaskResponse`: Full task object including all fields
- `TaskListResponse`: Array of TaskResponse objects
- `TaskOperationResponse`: Success/failure indicator with optional message

## Migration Strategy

### Initial Schema Creation
- Create tasks table with all required columns
- Set up indexes for performance
- Initialize with zero records

### Future Extensions
- Additional metadata fields can be added with nullable defaults
- Status enum can be extended with new values
- Soft-delete capability can be added if needed