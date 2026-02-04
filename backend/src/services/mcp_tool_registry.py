from typing import Dict, Any, Optional
from uuid import UUID
from datetime import datetime
import json
from ..models.task import Task, TaskCreate, TaskUpdate
from ..models.tool_call import ToolCall, ToolCallCreate
from sqlmodel import Session, select


class MCPTaskToolRegistry:
    """Registry for MCP tools that can be used by the OpenAI agent."""

    def __init__(self, session: Session):
        self.session = session

    def register_tools(self) -> Dict[str, callable]:
        """Register all available MCP tools."""
        return {
            "create_task": self.create_task,
            "list_tasks": self.list_tasks,
            "update_task": self.update_task,
            "complete_task": self.complete_task,
            "delete_task": self.delete_task
        }

    def create_task(self, title: str, description: Optional[str] = None, priority: str = "medium") -> Dict[str, Any]:
        """Create a new task via MCP tool."""
        try:
            task_create = TaskCreate(title=title, description=description, priority=priority)
            task = Task(**task_create.dict())

            self.session.add(task)
            self.session.flush()  # Flush to assign ID without committing yet
            task_id = task.id  # Store the ID before committing

            # Log the tool call
            tool_call = ToolCall(
                function_name="create_task",
                parameters={"title": title, "description": description, "priority": priority},
                result={"id": str(task.id), "title": task.title, "status": task.status},
                status="success",
                entity_id=task.id,
                entity_type="Task"
            )
            self.session.add(tool_call)

            # Now commit everything together
            self.session.commit()
            self.session.refresh(task)

            return {
                "id": str(task.id),
                "title": task.title,
                "description": task.description,
                "status": task.status,
                "priority": task.priority,
                "created_at": task.created_at.isoformat()
            }
        except Exception as e:
            # Log the error in tool call
            tool_call = ToolCall(
                function_name="create_task",
                parameters={"title": title, "description": description, "priority": priority},
                result={"error": str(e)},
                status="error"
            )
            self.session.add(tool_call)
            self.session.commit()

            raise e

    def list_tasks(self, status: Optional[str] = None, priority: Optional[str] = None) -> list:
        """List tasks with optional filtering."""
        try:
            statement = select(Task)
            if status:
                statement = statement.where(Task.status == status)
            if priority:
                statement = statement.where(Task.priority == priority)

            tasks = self.session.exec(statement).all()

            # Log the tool call
            tool_call = ToolCall(
                function_name="list_tasks",
                parameters={"status": status, "priority": priority},
                result={"count": len(tasks), "tasks": [{"id": str(t.id), "title": t.title, "status": t.status} for t in tasks]},
                status="success"
            )
            self.session.add(tool_call)
            self.session.commit()
            self.session.flush()

            return [
                {
                    "id": str(task.id),
                    "title": task.title,
                    "description": task.description,
                    "status": task.status,
                    "priority": task.priority,
                    "created_at": task.created_at.isoformat(),
                    "updated_at": task.updated_at.isoformat()
                } for task in tasks
            ]
        except Exception as e:
            # Log the error in tool call
            tool_call = ToolCall(
                function_name="list_tasks",
                parameters={"status": status, "priority": priority},
                result={"error": str(e)},
                status="error"
            )
            self.session.add(tool_call)
            self.session.commit()

            raise e

    def update_task(self, task_id: str = None, title: Optional[str] = None, description: Optional[str] = None,
                   status: Optional[str] = None, priority: Optional[str] = None) -> Dict[str, Any]:
        """Update an existing task."""
        try:
            # Find the task - either by ID or by title
            task = None

            if task_id:
                try:
                    task_uuid = UUID(task_id)
                    task = self.session.get(Task, task_uuid)
                except ValueError:
                    # If task_id is not a valid UUID, treat it as a title
                    statement = select(Task).where(Task.title == task_id)
                    task = self.session.exec(statement).first()
            elif title:
                # Find by title if no ID provided
                statement = select(Task).where(Task.title == title)
                task = self.session.exec(statement).first()

            if not task:
                raise ValueError("Task not found")

            # Update task fields
            if title is not None:
                task.title = title
            if description is not None:
                task.description = description
            if status is not None:
                task.status = status
            if priority is not None:
                task.priority = priority

            task.updated_at = datetime.utcnow()

            self.session.add(task)
            self.session.commit()
            self.session.refresh(task)

            # Log the tool call
            tool_call = ToolCall(
                function_name="update_task",
                parameters={"task_id": str(task.id) if task else task_id, "title": title, "description": description, "status": status, "priority": priority},
                result={"id": str(task.id), "title": task.title, "status": task.status},
                status="success",
                entity_id=task.id,
                entity_type="Task"
            )
            self.session.add(tool_call)
            self.session.commit()
            self.session.flush()

            return {
                "id": str(task.id),
                "title": task.title,
                "description": task.description,
                "status": task.status,
                "priority": task.priority,
                "updated_at": task.updated_at.isoformat()
            }
        except Exception as e:
            # Log the error in tool call
            tool_call = ToolCall(
                function_name="update_task",
                parameters={"task_id": task_id, "title": title, "description": description, "status": status, "priority": priority},
                result={"error": str(e)},
                status="error"
            )
            self.session.add(tool_call)
            self.session.commit()

            raise e

    def complete_task(self, task_id: str = None, title: Optional[str] = None) -> Dict[str, Any]:
        """Mark a task as completed."""
        try:
            # Find the task - either by ID or by title
            task = None

            if task_id:
                try:
                    task_uuid = UUID(task_id)
                    task = self.session.get(Task, task_uuid)
                except ValueError:
                    # If task_id is not a valid UUID, treat it as a title
                    statement = select(Task).where(Task.title == task_id)
                    task = self.session.exec(statement).first()
            elif title:
                # Find by title if no ID provided
                statement = select(Task).where(Task.title == title)
                task = self.session.exec(statement).first()

            if not task:
                raise ValueError("Task not found")

            task.status = "completed"
            task.completed_at = datetime.utcnow()
            task.updated_at = datetime.utcnow()

            self.session.add(task)
            self.session.commit()
            self.session.refresh(task)

            # Log the tool call
            tool_call = ToolCall(
                function_name="complete_task",
                parameters={"task_id": str(task.id) if task else task_id, "title": title},
                result={"id": str(task.id), "title": task.title, "status": task.status},
                status="success",
                entity_id=task.id,
                entity_type="Task"
            )
            self.session.add(tool_call)
            self.session.commit()
            self.session.flush()

            return {
                "id": str(task.id),
                "title": task.title,
                "status": task.status,
                "completed_at": task.completed_at.isoformat()
            }
        except Exception as e:
            # Log the error in tool call
            tool_call = ToolCall(
                function_name="complete_task",
                parameters={"task_id": task_id},
                result={"error": str(e)},
                status="error"
            )
            self.session.add(tool_call)
            self.session.commit()

            raise e

    def delete_task(self, task_id: str = None, title: Optional[str] = None) -> Dict[str, Any]:
        """Delete a task."""
        try:
            # Find the task - either by ID or by title
            task = None

            if task_id:
                try:
                    task_uuid = UUID(task_id)
                    task = self.session.get(Task, task_uuid)
                except ValueError:
                    # If task_id is not a valid UUID, treat it as a title
                    statement = select(Task).where(Task.title == task_id)
                    task = self.session.exec(statement).first()
            elif title:
                # Find by title if no ID provided
                statement = select(Task).where(Task.title == title)
                task = self.session.exec(statement).first()

            if not task:
                raise ValueError("Task not found")

            # Log the tool call before deletion
            tool_call = ToolCall(
                function_name="delete_task",
                parameters={"task_id": str(task.id) if task else task_id, "title": title},
                result={"id": str(task.id), "title": task.title, "status": task.status},
                status="success",
                entity_id=task.id,
                entity_type="Task"
            )
            self.session.add(tool_call)

            self.session.delete(task)
            self.session.commit()
            self.session.flush()

            return {
                "id": str(task.id),
                "title": task.title,
                "message": "Task deleted successfully"
            }
        except Exception as e:
            # Log the error in tool call
            tool_call = ToolCall(
                function_name="delete_task",
                parameters={"task_id": task_id},
                result={"error": str(e)},
                status="error"
            )
            self.session.add(tool_call)
            self.session.commit()

            raise e