#!/usr/bin/env python3
"""
Script to create a proper test user in the database with a known password.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.src.services.auth_service import get_password_hash
from backend.src.core.database import get_session_context
from backend.src.models.user import User
from datetime import datetime, timezone

def create_test_user():
    print("Creating a test user with known credentials...")

    # Test user data
    email = "testuser@example.com"
    password = "TestPassword123!"

    # Hash the password using the same method as the application
    try:
        hashed_password = get_password_hash(password)
        print(f"Password hashed successfully for {email}")
    except Exception as e:
        print(f"Error hashing password: {e}")
        return

    # Create user in database
    try:
        session_gen = get_session_context()
        session = next(session_gen)

        try:
            # Check if user already exists using the proper method
            from sqlmodel import select
            existing_user_result = session.exec(select(User).where(User.email == email)).first()
            if existing_user_result:
                print(f"User {email} already exists in database")
                print(f"   Email: {email}")
                print(f"   Password: {password}")
                print(f"   You can now use these credentials to log in.")
                return

            # Create new user
            current_time = datetime.now(timezone.utc)
            user = User(
                email=email,
                hashed_password=hashed_password,
                created_at=current_time,
                updated_at=current_time
            )

            session.add(user)
            session.commit()
            session.refresh(user)

            print(f"SUCCESS: Test user created successfully!")
            print(f"   Email: {email}")
            print(f"   Password: {password}")
            print(f"   You can now use these credentials to log in.")

        finally:
            try:
                next(session_gen)
            except StopIteration:
                pass

    except Exception as e:
        print(f"Error creating user: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    create_test_user()