import requests
import json

# Test creating a task through the chat API
BASE_URL = "http://127.0.0.1:8000"

# First, register a new test user
import time
timestamp = int(time.time())
test_email = f"chat_test_{timestamp}@example.com"
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

# Now test the chat endpoint with a specific request to create a task
print("\nTesting chat with task creation request...")
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# Send a message that should trigger task creation
chat_response = requests.post(f"{BASE_URL}/api/v1/chat", json={
    "user_input": "Please create a task titled 'Test Task from Chat' with description 'This task was created from the chat interface'",
    "conversation_id": None
}, headers=headers)

print(f"Chat response status: {chat_response.status_code}")
if chat_response.status_code == 200:
    response_data = chat_response.json()
    print(f"Response: {response_data['response']}")
    print(f"Tool execution result: {response_data.get('tool_execution_result')}")
else:
    print(f"Chat request failed: {chat_response.text}")

# Now check if the task was created in the database by listing tasks
print("\nChecking if task was created...")
tasks_response = requests.get(f"{BASE_URL}/api/tasks", headers=headers)

if tasks_response.status_code == 200:
    tasks = tasks_response.json()
    print(f"Number of tasks found: {len(tasks)}")
    for task in tasks:
        print(f"- Task: {task.get('title', 'No title')} (ID: {task.get('id', 'No ID')})")
else:
    print(f"Tasks request failed: {tasks_response.status_code} - {tasks_response.text}")