#!/usr/bin/env python3
"""
Script to update the database schema to add missing conversation_metadata column.
"""

import sqlite3
import sys
import os

def update_database_schema():
    db_path = "backend/chat_app.db"

    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}")
        return False

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Check if conversation_metadata column already exists
        cursor.execute("PRAGMA table_info(conversation);")
        columns = [col[1] for col in cursor.fetchall()]

        if 'conversation_metadata' in columns:
            print("conversation_metadata column already exists")
            return True

        # Add the conversation_metadata column
        print("Adding conversation_metadata column to conversation table...")
        cursor.execute("ALTER TABLE conversation ADD COLUMN conversation_metadata TEXT;")

        # Commit the changes
        conn.commit()
        print("Database schema updated successfully!")

        # Verify the change
        cursor.execute("PRAGMA table_info(conversation);")
        columns = cursor.fetchall()
        print("\nUpdated columns in conversation table:")
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")

        return True

    except Exception as e:
        print(f"Error updating database schema: {e}")
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    success = update_database_schema()
    if not success:
        sys.exit(1)