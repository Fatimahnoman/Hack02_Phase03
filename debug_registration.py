#!/usr/bin/env python3
"""
Debug script to identify the exact registration error with PostgreSQL.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.src.api.auth_router import register
from backend.src.models.user import UserCreate
from backend.src.core.database import get_session_context
from sqlmodel import Session
import traceback

def test_registration_debug():
    print("Testing registration directly with PostgreSQL database...")
    
    # Create a test user
    test_user = UserCreate(email="debug_test@example.com", password="TestPassword123!")
    
    # Create a database session
    session_gen = get_session_context()
    session = next(session_gen)
    
    try:
        # Attempt to register the user using the same function as the API
        result = register(test_user, session)
        print(f"[SUCCESS] Registration succeeded: {result}")
        return True
    except Exception as e:
        print(f"[ERROR] Registration failed with error: {str(e)}")
        print(f"Full traceback: {traceback.format_exc()}")
        return False
    finally:
        # Close the session properly
        try:
            next(session_gen)
        except StopIteration:
            pass

if __name__ == "__main__":
    test_registration_debug()