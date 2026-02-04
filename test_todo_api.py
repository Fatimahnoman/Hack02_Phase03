#!/usr/bin/env python3
"""
Test script to verify that the todo API endpoints are working correctly.
"""

import requests
import json

# Configuration
BASE_URL = "http://127.0.0.1:8000"

def test_todo_endpoints():
    print("Testing Todo API endpoints...")

    # First, try to register a test user
    print("\n1. Testing authentication endpoints...")
    try:
        # Attempt to register a test user
        register_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword123"
        }
        register_response = requests.post(f"{BASE_URL}/api/auth/register", json=register_data)
        print(f"Register response: {register_response.status_code}")

        if register_response.status_code == 200:
            auth_data = register_response.json()
            token = auth_data.get('access_token')
        else:
            # Try to login with existing user
            login_response = requests.post(f"{BASE_URL}/api/auth/login", json={
                "email": "test@example.com",
                "password": "testpassword123"
            })
            print(f"Login response: {login_response.status_code}")
            if login_response.status_code == 200:
                auth_data = login_response.json()
                token = auth_data.get('access_token')
            else:
                print("Could not authenticate. Please make sure you have a user account.")
                return

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        print(f"\n2. Testing todo creation...")
        # Test creating a todo
        todo_data = {
            "title": "Test Task",
            "description": "This is a test task created via API",
            "due_date": "2025-12-31T10:00:00"
        }

        create_response = requests.post(f"{BASE_URL}/api/todos/", json=todo_data, headers=headers)
        print(f"Create todo response: {create_response.status_code}")
        if create_response.status_code == 200:
            created_todo = create_response.json()
            print(f"Created todo: {created_todo}")
            todo_id = created_todo['id']

            print(f"\n3. Testing todo retrieval...")
            # Test getting all todos
            get_response = requests.get(f"{BASE_URL}/api/todos/", headers=headers)
            print(f"Get todos response: {get_response.status_code}")
            if get_response.status_code == 200:
                todos = get_response.json()
                print(f"Retrieved {len(todos)} todos")

            print(f"\n4. Testing todo update...")
            # Test updating a todo
            update_data = {
                "title": "Updated Test Task",
                "description": "This task has been updated"
            }
            update_response = requests.put(f"{BASE_URL}/api/todos/{todo_id}", json=update_data, headers=headers)
            print(f"Update todo response: {update_response.status_code}")

            print(f"\n5. Testing todo completion toggle...")
            # Test toggling completion status
            status_data = {"completed": True}
            toggle_response = requests.patch(f"{BASE_URL}/api/todos/{todo_id}/status", json=status_data, headers=headers)
            print(f"Toggle completion response: {toggle_response.status_code}")

            print(f"\n6. Testing todo deletion...")
            # Test deleting the todo
            delete_response = requests.delete(f"{BASE_URL}/api/todos/{todo_id}", headers=headers)
            print(f"Delete todo response: {delete_response.status_code}")

        else:
            print(f"Failed to create todo: {create_response.text}")

    except requests.exceptions.ConnectionError:
        print(f"Could not connect to the API at {BASE_URL}. Is the backend server running?")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    test_todo_endpoints()