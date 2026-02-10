import requests
import json
import time

# Test to see if the AI is properly calling the create_task function
BASE_URL = "http://127.0.0.1:8000"

# Register a new test user
timestamp = int(time.time())
test_email = f"tool_test_{timestamp}@example.com"
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

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# Test with a very explicit request to create a task
print("\nTesting with an explicit task creation request...")
chat_response = requests.post(f"{BASE_URL}/api/v1/chat", json={
    "user_input": "Please use the create_task function to add a task with title 'Operation' and description 'Heart surgery on 23 Feb 2026'",
    "conversation_id": None
}, headers=headers)

print(f"Chat response status: {chat_response.status_code}")
if chat_response.status_code == 200:
    response_data = chat_response.json()
    response_text = response_data['response']
    safe_response = response_text.encode('ascii', errors='replace').decode('ascii')
    print(f"Response: {safe_response}")
    
    # Check if there's tool execution result
    tool_result = response_data.get('tool_execution_result')
    if tool_result:
        print(f"Tool execution result: {tool_result}")
    else:
        print("No tool execution result found")
    
    # Check the tasks to see if it was created
    tasks_response = requests.get(f"{BASE_URL}/api/tasks", headers=headers)
    if tasks_response.status_code == 200:
        tasks = tasks_response.json()
        print(f"\nTotal tasks in database: {len(tasks)}")
        
        if tasks:
            # Find the task with 'Operation' in the title or description
            operation_task = None
            for task in reversed(tasks):
                if 'operation' in task.get('title', '').lower() or 'operation' in task.get('description', '').lower():
                    operation_task = task
                    break
            
            if operation_task:
                title = operation_task.get('title', '')
                description = operation_task.get('description', '')
                
                print(f"Found Operation task - Title: '{title}', Description: '{description}'")
                
                # Check if the task was created with the correct title and description
                if title.lower() == 'operation' and 'heart surgery' in description.lower() and '23 feb 2026' in description.lower():
                    print("SUCCESS: Task created with correct title and date in description!")
                elif 'operation' in title.lower() and '23 feb 2026' in title.lower():
                    print("PARTIAL SUCCESS: Task created but date is still in title")
                else:
                    print("RESULT: Task was created but not in the expected format")
            else:
                print("No Operation task found in the database")
        else:
            print("No tasks found in the database")
    else:
        print(f"Could not fetch tasks: {tasks_response.text}")
else:
    print(f"Request failed: {chat_response.text}")

print("\n" + "="*80)
print("ANALYSIS:")
print("If the AI is not calling the create_task function, it might be because:")
print("1. The AI model doesn't properly recognize function calling patterns")
print("2. The system prompt isn't directing the AI to use functions appropriately")
print("3. The AI prefers to respond directly rather than calling tools")
print("="*80)