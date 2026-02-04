#!/usr/bin/env python3
"""
Debug script to check which database file is being used.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.src.core.config import settings
from backend.src.core.database import engine
import sqlite3


def main():
    print("Checking database configuration...")
    print(f"Settings database_url: {settings.database_url}")

    # Extract the database file path from the URL
    if settings.database_url.startswith("sqlite:///"):
        db_path = settings.database_url[10:]  # Remove "sqlite:///" prefix
        print(f"Database file path: {db_path}")

        # Check if file exists
        if os.path.exists(db_path):
            print(f"V Database file exists: {os.path.abspath(db_path)}")

            # Check tables in the database
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            print(f"Tables in database: {[table[0] for table in tables]}")

            if 'task' in [table[0] for table in tables]:
                print("V Task table exists in database")

                # Count tasks
                cursor.execute("SELECT COUNT(*) FROM task;")
                count = cursor.fetchone()[0]
                print(f"Task count: {count}")

                # Show sample tasks
                cursor.execute("SELECT id, title, status FROM task LIMIT 5;")
                sample_tasks = cursor.fetchall()
                for task in sample_tasks:
                    print(f"  - {task[1]} (ID: {task[0]}, Status: {task[2]})")
            else:
                print("X Task table does not exist in database")

            conn.close()
        else:
            print(f"X Database file does NOT exist: {os.path.abspath(db_path)}")
    else:
        print("Not using SQLite database")


if __name__ == "__main__":
    main()