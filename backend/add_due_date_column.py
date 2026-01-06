import psycopg2
from urllib.parse import urlparse
import os
from src.config import settings

def add_due_date_column():
    """Add due_date column to the todo table"""
    try:
        # Parse the database URL
        result = urlparse(settings.database_url)

        conn = psycopg2.connect(
            host=result.hostname,
            database=result.path[1:],  # Remove the leading '/'
            user=result.username,
            password=result.password,
            port=result.port
        )

        cursor = conn.cursor()

        # Check if the column exists first
        cursor.execute("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name='todo' AND column_name='due_date'
        """)

        column_exists = cursor.fetchone()

        if not column_exists:
            # Add the due_date column to the todo table
            cursor.execute("""
                ALTER TABLE todo
                ADD COLUMN due_date TIMESTAMP WITH TIME ZONE DEFAULT NULL
            """)
            print("Successfully added due_date column to todo table")
        else:
            print("due_date column already exists")

        conn.commit()
        cursor.close()
        conn.close()

        print("Database schema updated successfully!")

    except Exception as e:
        print(f"Error updating database schema: {e}")

if __name__ == "__main__":
    add_due_date_column()