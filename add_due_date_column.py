#!/usr/bin/env python3
"""
Migration script to add due_date column to the task table.
"""

import sys
import os

# Add the backend src directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend', 'src'))

from sqlalchemy import text
from src.core.database import engine


def add_due_date_column():
    """Add due_date column to the task table."""
    print("Adding due_date column to the task table...")
    
    # Add the column directly to the database
    with engine.connect() as conn:
        # Check if column already exists
        result = conn.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'task' AND column_name = 'due_date'
        """))
        
        if result.fetchone():
            print("due_date column already exists.")
            return
        
        # Add the due_date column
        conn.execute(text("ALTER TABLE task ADD COLUMN due_date TIMESTAMP;"))
        conn.commit()
    
    print("due_date column added successfully!")


if __name__ == "__main__":
    add_due_date_column()