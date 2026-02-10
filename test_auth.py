#!/usr/bin/env python3
"""
Test script to verify user authentication.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.src.services.auth_service import authenticate_user, get_user_by_email
from backend.src.core.database import get_session_context
from sqlmodel import Session

def test_user_authentication():
    print("Testing user authentication...")
    
    # Create a session
    session_gen = get_session_context()
    session = next(session_gen)
    
    try:
        # Get all users to see what's available
        from sqlmodel import select
        from backend.src.models.user import User
        all_users = session.exec(select(User)).all()
        print(f"Total users in database: {len(all_users)}")
        
        for user in all_users:
            print(f"User ID: {user.id}, Email: {user.email}")
        
        # Test authenticating with a known user
        # Let's try with the first user
        if all_users:
            test_user = all_users[0]
            print(f"\nTesting authentication for user: {test_user.email}")
            
            # Try to authenticate with a common test password
            common_passwords = ["TestPassword123!", "password", "123456", "password123"]
            
            for pwd in common_passwords:
                auth_result = authenticate_user(session, test_user.email, pwd)
                if auth_result:
                    print(f"Authentication successful with password: {pwd}")
                    break
            else:
                print("Authentication failed with common passwords")
                
            # Test getting user by email directly
            user_by_email = get_user_by_email(session, test_user.email)
            print(f"get_user_by_email result: {user_by_email is not None}")
            
        else:
            print("No users found in database")
            
    except Exception as e:
        print(f"Error in user authentication test: {e}")
        import traceback
        traceback.print_exc()
    finally:
        next(session_gen)  # Close session

if __name__ == "__main__":
    test_user_authentication()