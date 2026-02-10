#!/usr/bin/env python3
"""
Comprehensive test to simulate the actual API registration process.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.src.api.auth_router import register, AuthResponse
from backend.src.models.user import UserCreate
from backend.src.core.database import get_session_context
from fastapi import HTTPException
import traceback
import asyncio

def test_api_registration():
    print("Testing API registration process...")
    
    # Create a test user
    test_user = UserCreate(email="api_test@example.com", password="TestPassword123!")
    
    try:
        # Simulate the API call to register function
        # Get a session using the same method as the API
        session_gen = get_session_context()
        session = next(session_gen)
        
        try:
            result = register(test_user, session)
            print(f"[SUCCESS] API registration succeeded: {result}")
            return True
        except HTTPException as he:
            print(f"[HTTP ERROR] Registration failed with HTTP error: {he.detail} (status: {he.status_code})")
            return False
        except Exception as e:
            print(f"[GENERAL ERROR] Registration failed with error: {str(e)}")
            print(f"Full traceback: {traceback.format_exc()}")
            return False
        finally:
            # Close the session properly
            try:
                next(session_gen)
            except StopIteration:
                pass
    except Exception as e:
        print(f"[SETUP ERROR] Error setting up registration test: {str(e)}")
        print(f"Full traceback: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    test_api_registration()