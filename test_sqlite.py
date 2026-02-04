#!/usr/bin/env python3
"""
Test script to check database configuration
"""

import os
from backend.src.core.config import settings

print("Current database URL:", settings.database_url)
print("Environment DATABASE_URL:", os.environ.get('DATABASE_URL', 'Not set'))

# Test creating a simple connection
from backend.src.core.database import engine
print("Engine URL:", str(engine.url))

# Test if we can connect to the database
from sqlmodel import select
from backend.src.core.database import get_session_context
from backend.src.models.user import User

try:
    session_gen = get_session_context()
    session = next(session_gen)

    # Try to query users
    stmt = select(User)
    users = session.exec(stmt).all()
    print(f"Connected successfully! Found {len(users)} users in database")

    # Print first few users
    for user in users[:3]:
        print(f"  - {user.email} (ID: {user.id})")

    next(session_gen)  # Close session
    print("Connection test completed successfully")

except Exception as e:
    print(f"Connection error: {e}")