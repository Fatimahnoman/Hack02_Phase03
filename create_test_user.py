#!/usr/bin/env python3
"""
Script to create a test user with a known password to verify authentication works.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.src.services.auth_service import create_user, authenticate_user
from backend.src.core.database import get_session_context
from backend.src.models.user import UserCreate
from sqlmodel import Session
import hashlib
import secrets


def create_test_user():
    """Create a test user with a known password."""
    
    print("Creating a test user with known credentials...")
    
    # Create a database session
    session_gen = get_session_context()
    session = next(session_gen)  # Get the session
    
    try:
        # Define test credentials
        test_email = "testuser@example.com"
        test_password = "password123"
        
        # Check if user already exists
        from backend.src.services.auth_service import get_user_by_email
        existing_user = get_user_by_email(session, test_email)
        
        if existing_user:
            print(f"Test user {test_email} already exists.")
            print(f"Attempting to authenticate with known password...")
            
            authenticated_user = authenticate_user(session, test_email, test_password)
            if authenticated_user:
                print(f"[SUCCESS] Successfully authenticated test user: {authenticated_user.email}")
                print(f"  User ID: {authenticated_user.id}")
            else:
                print(f"[FAILED] Failed to authenticate test user with known password")
                print(f"  This indicates the password might be different")
        else:
            # Create new test user
            user_create = UserCreate(email=test_email, password=test_password)
            created_user = create_user(session, user_create)
            print(f"[SUCCESS] Created test user: {created_user.email}")
            print(f"  User ID: {created_user.id}")
            
            # Verify we can authenticate with the new user
            authenticated_user = authenticate_user(session, test_email, test_password)
            if authenticated_user:
                print(f"[SUCCESS] Successfully authenticated new test user: {authenticated_user.email}")
            else:
                print(f"[FAILED] Failed to authenticate new test user")
    
    except Exception as e:
        print(f"Error during test user creation: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Close the session properly
        try:
            next(session_gen)  # This will trigger the finally block in the generator
        except StopIteration:
            pass  # Expected when the generator is exhausted


def test_with_real_user():
    """Try to authenticate with a real user using a common password."""
    print("\nTrying to authenticate with existing users using common passwords...")
    
    session_gen = get_session_context()
    session = next(session_gen)
    
    try:
        # Common passwords to try
        common_passwords = [
            "password", "password123", "123456", "admin", "letmein", 
            "welcome", "monkey", "1234567890", "qwerty", "abc123"
        ]
        
        # Get all users from the database
        from sqlmodel import select
        from backend.src.models.user import User
        stmt = select(User)
        users = session.exec(stmt).all()
        
        print(f"Found {len(users)} users in the database")
        
        for user in users:
            print(f"\nTrying to authenticate user: {user.email}")
            
            for password in common_passwords:
                authenticated_user = authenticate_user(session, user.email, password)
                if authenticated_user:
                    print(f"  [SUCCESS] Authenticated with password '{password}'")
                    break
            else:
                print(f"  [FAILED] None of the common passwords worked")
    
    except Exception as e:
        print(f"Error during real user authentication test: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        try:
            next(session_gen)
        except StopIteration:
            pass


if __name__ == "__main__":
    create_test_user()
    test_with_real_user()