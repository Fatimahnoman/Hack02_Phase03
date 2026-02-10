import requests
import json
import time

# Test the bot's ability to parse date information from task requests
BASE_URL = "http://127.0.0.1:8000"

# Register a new test user
timestamp = int(time.time())
test_email = f"direct_test_{timestamp}@example.com"
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

# Test with a very direct request
print("\nTesting with a direct task creation request...")
chat_response = requests.post(f"{BASE_URL}/api/v1/chat", json={
    "user_input": "Create a task with title 'Operation' and description 'Heart surgery on 23 Feb 2026'",
    "conversation_id": None
}, headers=headers)

print(f"Chat response status: {chat_response.status_code}")
if chat_response.status_code == 200:
    response_data = chat_response.json()
    response_text = response_data['response']
    safe_response = response_text.encode('ascii', errors='replace').decode('ascii')
    print(f"Response: {safe_response}")
    
    # Check the tasks to see how it was parsed
    tasks_response = requests.get(f"{BASE_URL}/api/tasks", headers=headers)
    if tasks_response.status_code == 200:
        tasks = tasks_response.json()
        print(f"\nTotal tasks in database: {len(tasks)}")
        
        if tasks:
            latest_task = tasks[-1]
            title = latest_task.get('title', '')
            description = latest_task.get('description', '')
            
            print(f"Latest task - Title: '{title}', Description: '{description}'")
            
            # Check if the task was created with the correct title and description
            if title.lower() == 'operation' and 'heart surgery' in description.lower() and '23 feb 2026' in description.lower():
                print("SUCCESS: Task created with correct title and date in description!")
            else:
                print("RESULT: Task was created but not in the expected format")
        else:
            print("No tasks found in the database")
    else:
        print(f"Could not fetch tasks: {tasks_response.text}")
else:
    print(f"Request failed: {chat_response.text}")

print("\n" + "="*80)
print("RECOMMENDED PROMPTS FOR DATE/TASK SEPARATION:")
print("="*80)
print("1. 'Create a task with title [TASK_NAME] and description [DESCRIPTION_WITH_DATE]'")
print("2. 'Add a task titled [TASK_NAME] about [DESCRIPTION_WITH_DATE]'")
print("3. 'Make a task called [TASK_NAME] for [DATE] with details [DESCRIPTION]'")
print("4. 'Create task [TASK_NAME] [DATE] - [DESCRIPTION]'")
print("5. 'New task: Title=[TASK_NAME], Date=[DATE], Description=[DESCRIPTION]'")
print("="*80)