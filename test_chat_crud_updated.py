#!/usr/bin/env python3
"""
Test script to access the chat route and perform CRUD operations.
"""

import requests
import json
import time

def test_chat_route():
    print("Testing chat route for CRUD operations...")
    
    # Assuming the server is running on localhost:8000
    base_url = "http://127.0.0.1:8000"
    
    # First, let's try to login to get an access token
    print("Step 1: Logging in to get access token...")
    login_data = {
        "email": "testuser@example.com",  # Using the test user we created
        "password": "TestPassword123!"    # Using the known password
    }
    
    try:
        login_response = requests.post(f"{base_url}/api/auth/login", json=login_data)
        print(f"Login response: {login_response.status_code}")
        
        if login_response.status_code == 200:
            token_data = login_response.json()
            access_token = token_data.get("access_token")
            print(f"Access token received: {access_token[:20]}...")
            
            # Set up headers with the token
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            print("\nStep 2: Testing chat route for task creation...")
            # Test creating a task via chat
            chat_data = {
                "user_input": "Add a task named 'Test Task from Chat' with description 'Created via chat route'",
                "user_id": "22"  # Using the user ID for testuser@example.com
            }
            
            chat_response = requests.post(f"{base_url}/api/v1/chat/", json=chat_data, headers=headers)
            print(f"Chat response: {chat_response.status_code}")
            print(f"Chat response body: {chat_response.text}")
            
            print("\nStep 3: Testing direct task listing (correct endpoint)...")
            # Test direct task listing - using the correct endpoint
            direct_list_response = requests.get(f"{base_url}/api/tasks", headers=headers)
            print(f"Direct task list response: {direct_list_response.status_code}")
            print(f"Direct task list body: {direct_list_response.text}")
            
            print("\nStep 4: Testing direct todo operations...")
            # Let's try the todo endpoints instead
            todo_data = {
                "title": "Test Todo from Direct API",
                "description": "Created via direct API call",
                "completed": False
            }
            
            todo_response = requests.post(f"{base_url}/api/todos/", json=todo_data, headers=headers)
            print(f"Direct todo creation response: {todo_response.status_code}")
            print(f"Direct todo creation body: {todo_response.text}")
            
            # List todos
            todos_response = requests.get(f"{base_url}/api/todos/", headers=headers)
            print(f"Direct todos list response: {todos_response.status_code}")
            print(f"Direct todos list body: {todos_response.text}")
            
        else:
            print(f"Login failed with status {login_response.status_code}")
            print(f"Login response: {login_response.text}")
            
    except Exception as e:
        print(f"Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_chat_route()