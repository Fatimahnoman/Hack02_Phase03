import requests
import json
import time

# Test the bot's ability to parse date information from task requests
BASE_URL = "http://127.0.0.1:8000"

# Register a new test user
timestamp = int(time.time())
test_email = f"date_parse_test_{timestamp}@example.com"
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

# Test the chat endpoint with a request that includes date information
print("\nTesting chat with date-containing task request...")
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# Send a request similar to what you described
chat_response = requests.post(f"{BASE_URL}/api/v1/chat", json={
    "user_input": "add task name operation on 23 feb 2026",
    "conversation_id": None
}, headers=headers)

print(f"Chat response status: {chat_response.status_code}")
if chat_response.status_code == 200:
    response_data = chat_response.json()
    response_text = response_data['response']
    safe_response = response_text.encode('ascii', errors='replace').decode('ascii')
    print(f"Response: {safe_response}")
else:
    print(f"Chat request failed: {chat_response.text}")

# Check if the task was created in the database with proper separation of name and date
print("\nChecking if task was created with proper name/date separation...")
tasks_response = requests.get(f"{BASE_URL}/api/tasks", headers=headers)

if tasks_response.status_code == 200:
    tasks = tasks_response.json()
    print(f"Number of tasks found: {len(tasks)}")
    
    # Find the task we just created (the one with date information)
    found_task = None
    for task in reversed(tasks):  # Go through tasks in reverse chronological order
        title = task.get('title', '').lower()
        description = task.get('description', '').lower()
        if 'operation' in title.lower() or '23 feb' in title.lower() or 'scheduled for' in description.lower():
            found_task = task
            break
    
    if found_task:
        print(f"Found our task:")
        print(f"  Title: {found_task.get('title', 'No title')}")
        print(f"  Description: {found_task.get('description', 'No description')}")
        print(f"  Status: {found_task.get('status', 'No status')}")
        
        # Check if the task was parsed correctly
        title = found_task.get('title', '').lower()
        description = found_task.get('description', '').lower()
        
        if ('operation' in title and ('23 feb' in description or 'scheduled for' in description.lower())) or \
           ('operation' in title and '2026' in description):
            print("\nSUCCESS: Task was correctly parsed!")
            print("   - Task name 'operation' extracted correctly")
            print("   - Date information moved to description/scheduling info")
        else:
            print("\nFAILURE: Task parsing may not have worked as expected")
            print("   The date information might still be part of the task title")
    else:
        print("Could not find the task we just created")
        print("Available tasks:")
        for i, task in enumerate(tasks[-5:], 1):  # Show last 5 tasks
            print(f"  {i}. Title: {task.get('title', 'No title')}, Description: {task.get('description', 'No description')}")
else:
    print(f"Tasks request failed: {tasks_response.status_code} - {tasks_response.text}")

print("\n" + "="*60)
print("EXAMPLE PROMPTS FOR BETTER DATE/TASK SEPARATION:")
print("="*60)
print("1. 'Create a task called [TASK_NAME] for [DATE]'")
print("2. 'Schedule [TASK_NAME] on [DATE]'") 
print("3. 'Add [TASK_NAME] to be done [DATE]'")
print("4. 'Set up [TASK_NAME] event for [DATE]'")
print("5. 'Remind me about [TASK_NAME] on [DATE]'")
print("6. 'Plan [TASK_NAME] activity for [DATE]'")
print("7. 'Book [TASK_NAME] appointment on [DATE]'")
print("8. 'Note down [TASK_NAME] to happen [DATE]'")
print("="*60)