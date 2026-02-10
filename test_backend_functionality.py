import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000"

def test_health_endpoint():
    """Test the health endpoint to verify the server is running."""
    print("Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Health check status: {response.status_code}")
        print(f"Health check response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error testing health endpoint: {e}")
        return False

def test_root_endpoint():
    """Test the root endpoint."""
    print("\nTesting root endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Root endpoint status: {response.status_code}")
        print(f"Root endpoint response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error testing root endpoint: {e}")
        return False

def test_user_registration():
    """Test user registration."""
    print("\nTesting user registration...")
    try:
        # Use a test email to avoid conflicts
        test_email = f"test_{int(time.time())}@example.com"
        payload = {
            "email": test_email,
            "password": "TestPassword123!"
        }
        response = requests.post(f"{BASE_URL}/api/auth/register", json=payload)
        print(f"Registration status: {response.status_code}")
        if response.status_code == 200:
            print(f"Registration response: {response.json()}")
            return True, test_email
        else:
            print(f"Registration error: {response.text}")
            return False, None
    except Exception as e:
        print(f"Error testing registration: {e}")
        return False, None

def test_user_login(email, password="TestPassword123!"):
    """Test user login."""
    print("\nTesting user login...")
    try:
        payload = {
            "email": email,
            "password": password
        }
        response = requests.post(f"{BASE_URL}/api/auth/login", json=payload)
        print(f"Login status: {response.status_code}")
        if response.status_code == 200:
            print(f"Login response: {response.json()}")
            token_data = response.json()
            return True, token_data.get("access_token")
        else:
            print(f"Login error: {response.text}")
            return False, None
    except Exception as e:
        print(f"Error testing login: {e}")
        return False, None

def test_chat_functionality(token):
    """Test chat functionality."""
    print("\nTesting chat functionality...")
    try:
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        payload = {
            "user_input": "Hello, can you help me buy groceries?",
            "conversation_id": None  # Will create new conversation
        }
        response = requests.post(f"{BASE_URL}/api/v1/chat", json=payload, headers=headers)
        print(f"Chat status: {response.status_code}")
        if response.status_code == 200:
            print(f"Chat response: {response.json()}")
            return True, response.json().get('conversation_id')
        else:
            print(f"Chat error: {response.text}")
            return False, None
    except Exception as e:
        print(f"Error testing chat functionality: {e}")
        return False, None

def test_todo_operations(token):
    """Test todo CRUD operations."""
    print("\nTesting todo operations...")
    try:
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        # Create a todo
        todo_payload = {
            "title": "Buy groceries",
            "description": "Milk, bread, eggs",
            "completed": False
        }
        response = requests.post(f"{BASE_URL}/api/todos/", json=todo_payload, headers=headers)
        print(f"Create todo status: {response.status_code}")
        if response.status_code == 200:
            print(f"Created todo: {response.json()}")
            todo_id = response.json().get("id")
            
            # Read the todo
            response = requests.get(f"{BASE_URL}/api/todos/{todo_id}", headers=headers)
            print(f"Read todo status: {response.status_code}")
            if response.status_code == 200:
                print(f"Read todo: {response.json()}")
                
                # Update the todo
                update_payload = {
                    "title": "Buy groceries - urgent",
                    "description": "Milk, bread, eggs, fruits",
                    "completed": True
                }
                response = requests.put(f"{BASE_URL}/api/todos/{todo_id}", json=update_payload, headers=headers)
                print(f"Update todo status: {response.status_code}")
                if response.status_code == 200:
                    print(f"Updated todo: {response.json()}")
                    
                    # Delete the todo
                    response = requests.delete(f"{BASE_URL}/api/todos/{todo_id}", headers=headers)
                    print(f"Delete todo status: {response.status_code}")
                    if response.status_code == 200:
                        print("Todo deleted successfully")
                        return True
        
        print(f"Todo error: {response.text}")
        return False
    except Exception as e:
        print(f"Error testing todo operations: {e}")
        return False

def test_task_operations(token):
    """Test task CRUD operations."""
    print("\nTesting task operations...")
    try:
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        # Create a task
        task_payload = {
            "title": "Grocery Shopping",
            "description": "Go to the supermarket and buy groceries",
            "status": "pending",
            "priority": "high"
        }
        response = requests.post(f"{BASE_URL}/api/tasks", json=task_payload, headers=headers)
        print(f"Create task status: {response.status_code}")
        if response.status_code == 200:
            print(f"Created task: {response.json()}")
            task_id = response.json().get("id")
            
            # Read the task
            response = requests.get(f"{BASE_URL}/api/tasks/{task_id}", headers=headers)
            print(f"Read task status: {response.status_code}")
            if response.status_code == 200:
                print(f"Read task: {response.json()}")
                
                # Update the task
                update_payload = {
                    "title": "Grocery Shopping - Completed",
                    "description": "Went to the supermarket and bought groceries",
                    "status": "completed",
                    "priority": "high"
                }
                response = requests.put(f"{BASE_URL}/api/tasks/{task_id}", json=update_payload, headers=headers)
                print(f"Update task status: {response.status_code}")
                if response.status_code == 200:
                    print(f"Updated task: {response.json()}")
                    
                    # Delete the task
                    response = requests.delete(f"{BASE_URL}/api/tasks/{task_id}", headers=headers)
                    print(f"Delete task status: {response.status_code}")
                    if response.status_code == 200:
                        print("Task deleted successfully")
                        return True
        
        print(f"Task error: {response.text}")
        return False
    except Exception as e:
        print(f"Error testing task operations: {e}")
        return False

def main():
    print("Starting backend functionality tests...\n")
    
    # Test 1: Health endpoint
    health_ok = test_health_endpoint()
    root_ok = test_root_endpoint()
    
    if not (health_ok and root_ok):
        print("\nServer is not responding. Please make sure the backend is running on http://127.0.0.1:8000")
        return
    
    # Test 2: User registration
    reg_success, email = test_user_registration()
    
    if not reg_success:
        print("\nRegistration failed. Stopping tests.")
        return
    
    # Test 3: User login
    login_success, token = test_user_login(email)
    
    if not login_success or not token:
        print("\nLogin failed. Stopping tests.")
        return
    
    # Test 4: Chat functionality
    chat_success, conv_id = test_chat_functionality(token)
    
    # Test 5: Todo operations
    todo_success = test_todo_operations(token)
    
    # Test 6: Task operations
    task_success = test_task_operations(token)
    
    print("\n" + "="*50)
    print("TEST SUMMARY:")
    print(f"Health endpoint: {'PASS' if health_ok else 'FAIL'}")
    print(f"Root endpoint: {'PASS' if root_ok else 'FAIL'}")
    print(f"User registration: {'PASS' if reg_success else 'FAIL'}")
    print(f"User login: {'PASS' if login_success else 'FAIL'}")
    print(f"Chat functionality: {'PASS' if chat_success else 'FAIL'}")
    print(f"Todo operations: {'PASS' if todo_success else 'FAIL'}")
    print(f"Task operations: {'PASS' if task_success else 'FAIL'}")
    print("="*50)

if __name__ == "__main__":
    main()