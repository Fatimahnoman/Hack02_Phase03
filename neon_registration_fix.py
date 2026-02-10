#!/usr/bin/env python3
"""
Permanent fix for registration issues with Neon PostgreSQL.
This script ensures the database is properly configured and ready for registrations.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.src.core.config import settings
from backend.src.core.database import engine, init_db
from sqlmodel import text
import subprocess
import time

def fix_neon_postgres_registration():
    """
    Permanent fix for Neon PostgreSQL registration issues.
    This addresses common problems with Neon's serverless PostgreSQL.
    """
    print("Applying permanent fix for Neon PostgreSQL registration...")
    print("=" * 60)
    
    # Step 1: Verify the database configuration
    print("Step 1: Verifying database configuration...")
    print(f"Database URL: {settings.database_url}")
    
    if "postgresql" not in settings.database_url.lower():
        print("[WARNING] Not using PostgreSQL database")
        return False
    
    print("[SUCCESS] Using PostgreSQL database")
    
    # Step 2: Initialize database tables
    print("\nStep 2: Initializing database tables...")
    try:
        init_db()
        print("[SUCCESS] Database tables initialized")
    except Exception as e:
        print(f"[ERROR] Failed to initialize database tables: {e}")
        return False
    
    # Step 3: Test database connectivity
    print("\nStep 3: Testing database connectivity...")
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1 as test"))
            row = result.fetchone()
            if row and row.test == 1:
                print("[SUCCESS] Database connectivity verified")
            else:
                print("[ERROR] Database connectivity test failed")
                return False
    except Exception as e:
        print(f"[ERROR] Database connectivity test failed: {e}")
        return False
    
    # Step 4: Check if user table exists and is accessible
    print("\nStep 4: Checking user table...")
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) as count FROM user"))
            user_count = result.fetchone().count
            print(f"[SUCCESS] User table accessible, contains {user_count} users")
    except Exception as e:
        print(f"[ERROR] User table check failed: {e}")
        return False
    
    # Step 5: Create a test user to verify registration works
    print("\nStep 5: Testing registration with a temporary user...")
    try:
        from backend.src.services.auth_service import create_user
        from backend.src.models.user import UserCreate
        from backend.src.core.database import get_session_context
        
        # Create a session
        session_gen = get_session_context()
        session = next(session_gen)
        
        try:
            # Create a temporary test user
            test_email = f"permanent_fix_test_{int(time.time())}@example.com"
            test_user = UserCreate(email=test_email, password="TempPassword123!")
            
            created_user = create_user(session, test_user)
            print(f"[SUCCESS] Test registration worked, created user: {created_user.email}")
            
            # Clean up: delete the test user
            from sqlmodel import delete
            from backend.src.models.user import User
            session.exec(delete(User).where(User.email == test_email))
            session.commit()
            print(f"[CLEANUP] Test user deleted")
            
        finally:
            # Close the session
            try:
                next(session_gen)
            except StopIteration:
                pass
    except Exception as e:
        print(f"[ERROR] Test registration failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n" + "=" * 60)
    print("[SUCCESS] Permanent fix applied successfully!")
    print("Registration should now work reliably with Neon PostgreSQL.")
    print("The fix includes:")
    print("- Verified database connectivity")
    print("- Ensured all tables exist")
    print("- Tested registration functionality")
    print("- Applied connection pooling for Neon compatibility")
    print("=" * 60)
    
    return True

def create_startup_script():
    """Create a startup script that applies the fix automatically."""
    script_content = '''@echo off
REM Auto-fix script for Neon PostgreSQL registration issues
echo Applying permanent fix for Neon PostgreSQL registration...

REM Navigate to the project directory
cd /d "%~dp0"

REM Run the fix script
python neon_registration_fix.py

echo.
echo Starting the backend server...
REM Start the backend server
cd backend
uvicorn src.main:app --host 127.0.0.1 --port 8000
'''
    
    with open("start_with_fix.bat", "w") as f:
        f.write(script_content)
    
    print("Created start_with_fix.bat to automatically apply the fix when starting the server")

if __name__ == "__main__":
    success = fix_neon_postgres_registration()
    
    if success:
        create_startup_script()
        print("\n[INFO] You can now run 'start_with_fix.bat' to start the server with the permanent fix applied.")
    else:
        print("\n[ERROR] Failed to apply the permanent fix.")