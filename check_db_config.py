#!/usr/bin/env python3
"""
Script to check which database URL the backend is actually using.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def check_database_config():
    print("Checking database configuration...")
    
    # Reload the config module to ensure fresh import
    if 'backend.src.core.config' in sys.modules:
        del sys.modules['backend.src.core.config']
    
    from backend.src.core.config import settings
    print(f"Database URL being used: {settings.database_url}")
    
    # Check if the SQLite file exists relative to the expected path
    import sqlite3
    db_path = "../test.db"  # As specified in our .env.local
    
    # Check from the backend directory
    backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
    full_path = os.path.join(backend_dir, db_path)
    print(f"Expected SQLite path (relative to backend): {full_path}")
    
    if os.path.exists(full_path):
        print("[SUCCESS] SQLite database file exists")

        # Check tables in the database
        conn = sqlite3.connect(full_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"Tables in database: {[table[0] for table in tables]}")
        conn.close()
    else:
        print("[ERROR] SQLite database file does not exist at the expected location")

        # Check from the current directory
        alt_path = os.path.join(os.path.dirname(__file__), "test.db")
        print(f"Checking for database at current directory: {alt_path}")
        if os.path.exists(alt_path):
            print("[SUCCESS] SQLite database exists at project root")

            # Check tables in the database
            conn = sqlite3.connect(alt_path)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            print(f"Tables in database: {[table[0] for table in tables]}")
            conn.close()
        else:
            print("[ERROR] SQLite database does not exist at project root either")

if __name__ == "__main__":
    check_database_config()