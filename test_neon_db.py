#!/usr/bin/env python3
"""
Test script to check if the Neon PostgreSQL database connection works.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.src.core.config import settings
from backend.src.core.database import engine
from sqlmodel import text
import asyncio

async def test_db_connection():
    print("Testing Neon PostgreSQL connection...")
    print(f"Database URL: {settings.database_url}")
    
    try:
        # Test the connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1 as test"))
            row = result.fetchone()
            print(f"Connection successful! Result: {row.test}")
            
            # Check if user table exists
            result = conn.execute(text("""
                SELECT EXISTS (
                   SELECT FROM information_schema.tables 
                   WHERE table_schema = 'public' 
                   AND table_name = 'user'
                ) as table_exists;
            """))
            table_exists = result.fetchone().table_exists
            print(f"User table exists: {table_exists}")
            
            if table_exists:
                # Count users
                result = conn.execute(text("SELECT COUNT(*) as count FROM \"user\""))
                user_count = result.fetchone().count
                print(f"Number of users in database: {user_count}")
                
                if user_count > 0:
                    # Get a sample user
                    result = conn.execute(text("SELECT id, email FROM \"user\" LIMIT 1"))
                    user = result.fetchone()
                    print(f"Sample user: ID={user.id}, Email={user.email}")
            
            return True
    except Exception as e:
        print(f"Connection failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_db_connection())
    if success:
        print("\nDatabase connection is working properly!")
    else:
        print("\nDatabase connection failed. Please check your Neon database configuration.")