import requests
import json
import time

# Test creating a task through the chat API with the specific request
BASE_URL = "http://127.0.0.1:8000"

# Register a new test user
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

# Now test the chat endpoint with the specific request
print("\nTesting chat with specific task creation request...")
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# Send the specific message you mentioned
chat_response = requests.post(f"{BASE_URL}/api/v1/chat", json={
    "user_input": "add one more task name makeup with description lipstick and will buy it on 23 march",
    "conversation_id": None
}, headers=headers)

print(f"Chat response status: {chat_response.status_code}")
if chat_response.status_code == 200:
    response_data = chat_response.json()
    response_text = response_data['response']
    safe_response = response_text.encode('ascii', errors='replace').decode('ascii')
    print(f"Response: {safe_response}")
    tool_result = response_data.get('tool_execution_result')
    if tool_result:
        safe_tool_result = str(tool_result).encode('ascii', errors='replace').decode('ascii')
        print(f"Tool execution result: {safe_tool_result}")
    else:
        print("No tool execution result")
else:
    print(f"Chat request failed: {chat_response.text}")

# Check if the task was created in the database
print("\nChecking if task was created...")
tasks_response = requests.get(f"{BASE_URL}/api/tasks", headers=headers)

if tasks_response.status_code == 200:
    tasks = tasks_response.json()
    print(f"Number of tasks found: {len(tasks)}")
    for task in tasks:
        print(f"- Task: {task.get('title', 'No title')} (ID: {task.get('id', 'No ID')})")
        print(f"  Description: {task.get('description', 'No description')}")
        print(f"  Status: {task.get('status', 'No status')}")
        print(f"  Priority: {task.get('priority', 'No priority')}")
else:
    print(f"Tasks request failed: {tasks_response.status_code} - {tasks_response.text}")