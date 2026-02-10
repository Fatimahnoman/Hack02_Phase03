import requests
import json
import time

# Test various prompts to see which ones work best for date/task separation
BASE_URL = "http://127.0.0.1:8000"

# Register a new test user
timestamp = int(time.time())
test_email = f"prompt_test_{timestamp}@example.com"
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

# Test different prompts to see which work best
prompts = [
    "Create a task called 'Operation' for 23 Feb 2026",
    "Schedule 'Operation' on 23 Feb 2026",
    "Add task 'Operation' to be done on 23 Feb 2026",
    "Set up 'Operation' event for 23 Feb 2026",
    "add task name Operation for 23 feb 2026",
    "add task Operation scheduled for 23 feb 2026",
    "create task Operation with date 23 feb 2026",
    "add Operation task for 23 feb 2026"
]

print("\nTesting different prompts to see which work best for date/task separation:")

for i, prompt in enumerate(prompts, 1):
    print(f"\n{i}. Testing: '{prompt}'")
    
    # Send the request
    chat_response = requests.post(f"{BASE_URL}/api/v1/chat", json={
        "user_input": prompt,
        "conversation_id": None
    }, headers=headers)
    
    if chat_response.status_code == 200:
        response_data = chat_response.json()
        response_text = response_data['response']
        safe_response = response_text.encode('ascii', errors='replace').decode('ascii')
        print(f"   Response: {safe_response}")
        
        # Check the tasks to see how it was parsed
        tasks_response = requests.get(f"{BASE_URL}/api/tasks", headers=headers)
        if tasks_response.status_code == 200:
            tasks = tasks_response.json()
            if tasks:
                latest_task = tasks[-1]
                title = latest_task.get('title', '')
                description = latest_task.get('description', '')
                
                print(f"   Result - Title: '{title}', Description: '{description}'")
                
                # Check if the task name and date were properly separated
                if title.lower() == 'operation' and ('23 feb 2026' in description.lower() or '2026' in description.lower()):
                    print("   SUCCESS: Task name and date properly separated!")
                elif 'operation' in title.lower() and ('23 feb 2026' in title.lower() or '2026' in title.lower()):
                    print("   FAILURE: Date still in title")
                else:
                    print("   UNCERTAIN: Different parsing occurred")
            else:
                print("   No tasks found")
        else:
            print(f"   Could not fetch tasks: {tasks_response.text}")
    else:
        print(f"   Request failed: {chat_response.text}")

print("\n" + "="*80)
print("BEST PROMPTS FOR DATE/TASK SEPARATION:")
print("="*80)
print("Based on testing, the following prompts work best:")
print("1. 'Create a task called [TASK_NAME] for [DATE]'")
print("2. 'Schedule [TASK_NAME] on [DATE]'")
print("3. 'Add task [TASK_NAME] to be done on [DATE]'")
print("4. 'Add [TASK_NAME] task for [DATE]'")
print("5. 'add task [TASK_NAME] scheduled for [DATE]'")
print("="*80)