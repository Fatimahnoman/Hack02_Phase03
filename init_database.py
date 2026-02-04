#!/usr/bin/env python3
"""
Script to initialize the database and create all required tables.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.src.core.database import init_db


def main():
    print("Initializing database and creating tables...")

    try:
        init_db()
        print("Database initialization completed successfully!")

        # Verify tables were created
        from backend.src.core.database import get_session_context
        from backend.src.models.task import Task
        from sqlmodel import select

        session_gen = get_session_context()
        session = next(session_gen)

        try:
            # Try to query tasks (should work now)
            statement = select(Task)
            tasks = session.exec(statement).all()
            print(f"Successfully connected to database. Found {len(tasks)} tasks.")

            if tasks:
                print("Sample tasks:")
                for i, task in enumerate(tasks[:3]):
                    print(f"  - {task.title} (ID: {task.id})")

        except Exception as e:
            print(f"Error querying tasks: {e}")
        finally:
            try:
                next(session_gen)
            except StopIteration:
                pass

    except Exception as e:
        print(f"Error during database initialization: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()