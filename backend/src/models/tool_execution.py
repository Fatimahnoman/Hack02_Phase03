"""Tool Execution model for tracking tool usage in stateless chatbot operations."""

from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel
import uuid


class ToolExecutionBase(SQLModel):
    """Base model for ToolExecution containing shared attributes."""
    intent_log_id: str = Field(foreign_key="intentlog.id")  # Foreign key linking to IntentLog
    tool_name: str = Field(sa_column_kwargs={"nullable": False})  # Name of the executed tool
    input_parameters: Optional[str] = Field(default=None)  # JSON serialized input parameters
    execution_result: Optional[str] = Field(default=None)  # JSON serialized result returned by the tool
    execution_status: str = Field(sa_column_kwargs={"nullable": False})  # ['success', 'failure', 'partial']
    error_message: Optional[str] = Field(default=None)  # Error details if execution failed


class ToolExecution(ToolExecutionBase, table=True):
    """ToolExecution model tracking all tool executions for validation and debugging."""

    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    executed_at: datetime = Field(default_factory=datetime.utcnow)  # Timestamp of tool execution

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if 'id' not in kwargs or kwargs['id'] is None:
            self.id = str(uuid.uuid4())
        if 'executed_at' not in kwargs or kwargs['executed_at'] is None:
            self.executed_at = datetime.utcnow()


class ToolExecutionCreate(ToolExecutionBase):
    """Schema for creating a new tool execution record."""
    pass


class ToolExecutionRead(ToolExecutionBase):
    """Schema for reading tool execution data."""
    id: str
    executed_at: datetime