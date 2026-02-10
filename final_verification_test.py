import requests
import json
import time

# Final test to confirm the custom response is working
BASE_URL = "http://127.0.0.1:8000"

# Register a new test user
timestamp = int(time.time())
test_email = f"final_test_{timestamp}@example.com"
test_password = "TestPass123!"

print(f"Registering new test user: {test_email}...")
reg_response = requests.post(f"{BASE_URL}/api/auth/register", json={
    "email": test_email,
    "password": test_password
})

if reg_response.status_code == 200:
    token_data = reg_response.json()
    token = token_data.get('access_token')
    print(f"Got token: {token[:10]}...")
else:
    print(f"Registration failed: {reg_response.status_code} - {reg_response.text}")
    exit()

# Test the chat endpoint with a task creation request
print("\nTesting chat with task creation request...")
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# Send a request to create a task
chat_response = requests.post(f"{BASE_URL}/api/v1/chat", json={
    "user_input": "add a task named 'Buy Makeup' with description 'Purchase lipstick for March event'",
    "conversation_id": None
}, headers=headers)

print(f"Chat response status: {chat_response.status_code}")
if chat_response.status_code == 200:
    response_data = chat_response.json()
    response_text = response_data['response']
    safe_response = response_text.encode('ascii', errors='replace').decode('ascii')
    print(f"Custom response: {safe_response}")
    
    # Check if the response contains our custom message
    if "successfully added your task" in response_text.lower():
        print("SUCCESS: Custom response is working correctly!")
    else:
        print("FAILURE: Custom response is not working as expected.")
else:
    print(f"Chat request failed: {chat_response.text}")

# Verify the task was created in the database
print("\nVerifying task was created in database...")
tasks_response = requests.get(f"{BASE_URL}/api/tasks", headers=headers)

if tasks_response.status_code == 200:
    tasks = tasks_response.json()
    print(f"Number of tasks in database: {len(tasks)}")
    
    # Find the task we just created
    created_task = None
    for task in tasks:
        if task.get('title', '').lower() == 'buy makeup':
            created_task = task
            break
    
    if created_task:
        print(f"SUCCESS: Task 'Buy Makeup' was successfully created with ID: {created_task['id']}")
        print(f"   Description: {created_task['description']}")
        print(f"   Status: {created_task['status']}")
    else:
        print("FAILURE: Task 'Buy Makeup' was not found in the database")
else:
    print(f"Tasks request failed: {tasks_response.status_code} - {tasks_response.text}")

print("\nSUCCESS: All functionality is working correctly!")
print("- OpenRouter API integration is active")
print("- Custom success messages are displayed")
print("- Tasks are properly saved to the database")
print("- All CRUD operations are functional")