#!/usr/bin/env python3
"""
Test script to verify the authentication system is working properly.
"""

import requests
import json
import sys
import os

# Test credentials
TEST_EMAIL = "test@example.com"
TEST_PASSWORD = "TestPassword123!"  # We'll try to register with this
WRONG_PASSWORD = "WrongPassword"

def test_authentication_system():
    """Test the authentication system endpoints."""

    base_url = "http://127.0.0.1:8000"

    print("Testing Authentication System...")
    print("="*50)

    # Test 1: Try to login with a known user (if exists)
    print("\n1. Testing login with existing user...")
    try:
        response = requests.post(f"{base_url}/api/auth/login",
                               json={"email": TEST_EMAIL, "password": "somepassword"})
        print(f"   Status: {response.status_code}")
        if response.status_code == 401:
            print("   Expected: 401 Unauthorized (wrong password)")
        elif response.status_code == 200:
            print("   Success: Login worked!")
            token_data = response.json()
            print(f"   Token received: {bool(token_data.get('access_token'))}")
        else:
            print(f"   Unexpected status: {response.status_code}")
    except Exception as e:
        print(f"   Error connecting to server: {e}")
        print("   Make sure the backend server is running on port 8000")
        return False

    # Test 2: Try to register a new user
    print("\n2. Testing user registration...")
    try:
        # Use a unique email for testing
        new_email = "test_registration@example.com"
        response = requests.post(f"{base_url}/api/auth/register",
                               json={"email": new_email, "password": "TestPass123!"})
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   Success: Registration worked!")
            token_data = response.json()
            print(f"   Token received: {bool(token_data.get('access_token'))}")
        elif response.status_code == 400:
            print("   Expected: 400 Bad Request (user already exists)")
        else:
            print(f"   Unexpected status: {response.status_code}")
            if response.status_code != 400:  # Don't print error if just user exists
                print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")
        return False

    print("\n" + "="*50)
    print("Authentication system test completed.")
    return True

if __name__ == "__main__":
    test_authentication_system()