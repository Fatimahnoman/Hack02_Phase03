#!/usr/bin/env python3
"""
Script to update the message table schema to add missing tool_call_id column.
"""

import sqlite3
import sys
import os

def update_message_table_schema():
    db_path = "backend/chat_app.db"

    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}")
        return False

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Check if tool_call_id column already exists
        cursor.execute("PRAGMA table_info(message);")
        columns = [col[1] for col in cursor.fetchall()]

        if 'tool_call_id' in columns:
            print("tool_call_id column already exists")
            return True

        # Add the tool_call_id column
        print("Adding tool_call_id column to message table...")
        cursor.execute("ALTER TABLE message ADD COLUMN tool_call_id CHAR(32);")

        # Commit the changes
        conn.commit()
        print("Message table schema updated successfully!")

        # Verify the change
        cursor.execute("PRAGMA table_info(message);")
        columns = cursor.fetchall()
        print("\nUpdated columns in message table:")
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")

        return True

    except Exception as e:
        print(f"Error updating message table schema: {e}")
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    success = update_message_table_schema()
    if not success:
        sys.exit(1)