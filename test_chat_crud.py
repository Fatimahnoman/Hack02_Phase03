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
                "user_id": "10"  # Using the user ID for fatimahnoman@gmail.com
            }
            
            chat_response = requests.post(f"{base_url}/api/v1/chat/", json=chat_data, headers=headers)
            print(f"Chat response: {chat_response.status_code}")
            print(f"Chat response body: {chat_response.text}")
            
            print("\nStep 3: Testing chat route for listing tasks...")
            # Test listing tasks via chat
            list_chat_data = {
                "user_input": "List all my tasks",
                "user_id": "10"
            }
            
            list_response = requests.post(f"{base_url}/api/v1/chat/", json=list_chat_data, headers=headers)
            print(f"List chat response: {list_response.status_code}")
            print(f"List chat response body: {list_response.text}")
            
            print("\nStep 4: Testing direct task creation for comparison...")
            # Also test direct task creation to compare
            task_data = {
                "title": "Direct Task Creation Test",
                "description": "This was created via direct API call",
                "status": "pending",
                "priority": "medium"
            }
            
            direct_task_response = requests.post(f"{base_url}/api/tasks/tasks", json=task_data, headers=headers)
            print(f"Direct task creation response: {direct_task_response.status_code}")
            print(f"Direct task creation body: {direct_task_response.text}")
            
            print("\nStep 5: Testing direct task listing for comparison...")
            # Test direct task listing
            direct_list_response = requests.get(f"{base_url}/api/tasks/tasks", headers=headers)
            print(f"Direct task list response: {direct_list_response.status_code}")
            print(f"Direct task list body: {direct_list_response.text[:500]}...")  # Truncate for readability
            
        else:
            print(f"Login failed with status {login_response.status_code}")
            print(f"Login response: {login_response.text}")
            
            # Let's try to access the chat route without authentication to see if it works
            print("\nTrying chat route without authentication...")
            chat_data = {
                "user_input": "Say hello",
                "user_id": None
            }
            
            chat_response = requests.post(f"{base_url}/api/v1/chat/", json=chat_data)
            print(f"Chat response (no auth): {chat_response.status_code}")
            print(f"Chat response body: {chat_response.text}")
            
    except Exception as e:
        print(f"Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_chat_route()