#!/usr/bin/env python3
"""
Script to create a test user in the database for login testing.
"""

import sqlite3
from datetime import datetime
from passlib.context import CryptContext

# Initialize the password context (same as in auth_service.py)
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# Connect to the database
conn = sqlite3.connect('test.db')
cursor = conn.cursor()

# Test user data
email = "fatimah.noman@gmail.com"
password = "TestPassword123!"  # Strong test password

# Hash the password using the same method as the application
hashed_password = pwd_context.hash(password)

# Insert the user into the database
try:
    cursor.execute("""
        INSERT INTO user (email, hashed_password, created_at, updated_at)
        VALUES (?, ?, ?, ?)
    """, (email, hashed_password, datetime.utcnow(), datetime.utcnow()))

    conn.commit()
    print(f"User {email} created successfully!")
    print(f"Password: {password}")
    print("You can now try to log in with these credentials.")

except sqlite3.IntegrityError as e:
    print(f"Error creating user: {e}")
    print("User might already exist.")

finally:
    conn.close()