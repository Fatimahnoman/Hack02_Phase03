#!/usr/bin/env python3
"""
Test script to verify that tasks created via the chatbot are properly saved to the database
and accessible to the web application.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.src.core.database import get_session
from backend.src.models.task import Task
from sqlmodel import select
import uuid


def test_database_connection():
    """Test database connection and task retrieval."""
    print("Testing database connection...")

    try:
        # Use the same session mechanism as the backend
        from backend.src.core.database import get_session_context

        # Get a session using the context manager
        session_gen = get_session_context()
        session = next(session_gen)

        try:
            # Query all tasks
            statement = select(Task)
            tasks = session.exec(statement).all()

            print(f"Found {len(tasks)} tasks in the database:")
            for i, task in enumerate(tasks[:5]):  # Show first 5 tasks
                print(f"  {i+1}. ID: {task.id}, Title: '{task.title}', Status: {task.status}, Priority: {task.priority}")

            if len(tasks) > 5:
                print(f"  ... and {len(tasks) - 5} more tasks")

            return len(tasks)

        finally:
            # Close the session
            try:
                next(session_gen)
            except StopIteration:
                pass

    except Exception as e:
        print(f"Error connecting to database: {e}")
        import traceback
        traceback.print_exc()
        return 0


def test_task_creation():
    """Test creating a task directly through the backend models."""
    print("\nTesting task creation...")

    try:
        from backend.src.core.database import get_session_context
        from backend.src.models.task import Task, TaskCreate

        # Get a session
        session_gen = get_session_context()
        session = next(session_gen)

        try:
            # Create a test task
            test_task = TaskCreate(
                title="Test Task from Direct API",
                description="This task was created directly through the backend API to test database connectivity",
                priority="medium"
            )

            # Create the task object
            task = Task(**test_task.dict())

            # Add to session and commit
            session.add(task)
            session.commit()
            session.refresh(task)

            print(f"Successfully created task with ID: {task.id}")
            print(f"Task details - Title: '{task.title}', Status: {task.status}, Priority: {task.priority}")

            return task.id

        finally:
            # Close the session
            try:
                next(session_gen)
            except StopIteration:
                pass

    except Exception as e:
        print(f"Error creating task: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    print("=== Database Connectivity Test ===")

    # Test current database state
    task_count_before = test_database_connection()

    # Create a test task
    new_task_id = test_task_creation()

    if new_task_id:
        print("\nRe-checking database after task creation:")
        task_count_after = test_database_connection()

        if task_count_after > task_count_before:
            print(f"\n✓ SUCCESS: Database connectivity verified!")
            print(f"  - Tasks before: {task_count_before}")
            print(f"  - Tasks after: {task_count_after}")
            print(f"  - Successfully created test task: {new_task_id}")
            print("\nThe chatbot and web app should now use the same database.")
        else:
            print(f"\n⚠ WARNING: Task count didn't increase as expected")
    else:
        print(f"\n✗ FAILED: Could not create test task")
        print("There may still be database connection issues.")