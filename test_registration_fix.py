#!/usr/bin/env python3
"""
Test script to verify user registration works with the local database.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

import requests
import uuid
from datetime import datetime, timezone

def test_registration():
    print("Testing user registration...")

    # Generate a unique email for testing
    test_email = f"test_{uuid.uuid4().hex[:8]}@example.com"
    test_password = "TestPassword123!"
    
    print(f"Registering user: {test_email}")
    
    # Try to register a new user
    try:
        # First, let's try to run the backend server to test the API
        import subprocess
        import time
        
        # Start the backend server in the background
        server_process = subprocess.Popen([
            "uvicorn", "backend.src.main:app", 
            "--host", "127.0.0.1", 
            "--port", "8000", 
            "--reload"
        ], cwd=os.getcwd())
        
        # Wait a moment for the server to start
        time.sleep(5)
        
        # Test the registration endpoint
        registration_data = {
            "email": test_email,
            "password": test_password
        }
        
        response = requests.post("http://127.0.0.1:8000/api/auth/register", json=registration_data)
        
        if response.status_code == 200:
            print(f"[SUCCESS] User registered successfully: {test_email}")
            print(f"Response: {response.json()}")
            
            # Try to login with the new user
            login_data = {
                "email": test_email,
                "password": test_password
            }
            
            login_response = requests.post("http://127.0.0.1:8000/api/auth/login", json=login_data)
            
            if login_response.status_code == 200:
                print(f"[SUCCESS] User logged in successfully: {test_email}")
                print(f"Login response: {login_response.json()}")
            else:
                print(f"[ERROR] Login failed: {login_response.status_code} - {login_response.text}")
                
        else:
            print(f"[ERROR] Registration failed: {response.status_code} - {response.text}")
        
        # Terminate the server process
        server_process.terminate()
        
    except Exception as e:
        print(f"Error during registration test: {e}")
        import traceback
        traceback.print_exc()

def test_direct_database_connection():
    """Test connecting to the database directly using the auth service."""
    print("\nTesting direct database connection...")
    
    try:
        from backend.src.core.database import get_session_context
        from backend.src.services.auth_service import create_user, get_user_by_email
        from backend.src.models.user import UserCreate
        from sqlmodel import Session
        import uuid
        
        # Create a unique test user
        test_email = f"direct_test_{uuid.uuid4().hex[:8]}@example.com"
        test_password = "TestPassword123!"
        
        # Create a database session
        session_gen = get_session_context()
        session = next(session_gen)  # Get the session
        
        try:
            # Check if user already exists
            existing_user = get_user_by_email(session, test_email)
            if existing_user:
                print(f"User {test_email} already exists.")
                return
            
            # Create new user
            user_create = UserCreate(email=test_email, password=test_password)
            created_user = create_user(session, user_create)
            print(f"[SUCCESS] Created user via auth service: {created_user.email}")
            print(f"  User ID: {created_user.id}")
            
            # Verify we can retrieve the user
            retrieved_user = get_user_by_email(session, test_email)
            if retrieved_user:
                print(f"[SUCCESS] Retrieved user from database: {retrieved_user.email}")
            else:
                print(f"[ERROR] Could not retrieve user from database")
                
        except Exception as e:
            print(f"[ERROR] Direct database operation failed: {e}")
            import traceback
            traceback.print_exc()
        finally:
            # Close the session properly
            try:
                next(session_gen)  # This will trigger the finally block in the generator
            except StopIteration:
                pass  # Expected when the generator is exhausted
                
    except Exception as e:
        print(f"[ERROR] Could not import backend modules: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_direct_database_connection()
    # Note: Commenting out the API test for now as it requires the server to be running
    # test_registration()