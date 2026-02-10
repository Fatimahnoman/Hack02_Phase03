#!/usr/bin/env python3
"""
Neon PostgreSQL connection health checker and initializer.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.src.core.config import settings
from backend.src.core.database import engine
from sqlmodel import text
import logging

def check_neon_connection():
    """Check if the Neon PostgreSQL connection is healthy."""
    print("Checking Neon PostgreSQL connection...")
    
    try:
        with engine.connect() as conn:
            # Execute a simple query to test the connection
            result = conn.execute(text("SELECT 1 as test"))
            row = result.fetchone()
            
            if row and row.test == 1:
                print("[SUCCESS] Connection to Neon PostgreSQL is healthy")
                
                # Check if tables exist
                result = conn.execute(text("""
                    SELECT tablename 
                    FROM pg_tables 
                    WHERE schemaname = 'public'
                """))
                tables = [row.tablename for row in result.fetchall()]
                
                print(f"Tables in database: {tables}")
                
                if 'user' in tables:
                    # Check if there are any users
                    user_result = conn.execute(text("SELECT COUNT(*) as count FROM user"))
                    user_count = user_result.fetchone().count
                    print(f"Number of users in database: {user_count}")
                
                return True
            else:
                print("[ERROR] Unexpected result from test query")
                return False
    except Exception as e:
        print(f"[ERROR] Connection to Neon PostgreSQL failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def ensure_tables_exist():
    """Ensure all required tables exist in the database."""
    print("Ensuring all required tables exist...")
    
    try:
        from backend.src.core.database import init_db
        init_db()
        print("[SUCCESS] Tables verified/created successfully")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to ensure tables exist: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("Neon PostgreSQL Health Check and Setup")
    print("=" * 50)
    
    # Check the connection
    connection_ok = check_neon_connection()
    
    if not connection_ok:
        print("\n[CRITICAL] Cannot connect to Neon PostgreSQL database.")
        print("Please verify your DATABASE_URL in the .env file is correct.")
        return False
    
    # Ensure tables exist
    tables_ok = ensure_tables_exist()
    
    if not tables_ok:
        print("\n[CRITICAL] Failed to ensure database tables exist.")
        return False
    
    print("\n[SUCCESS] Neon PostgreSQL database is properly configured and healthy!")
    print("Registration should now work reliably.")
    
    return True

if __name__ == "__main__":
    main()