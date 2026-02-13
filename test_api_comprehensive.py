import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get the API URL
API_URL = os.getenv('NEXT_PUBLIC_API_URL', 'http://127.0.0.1:8000')
print(f"Testing API at: {API_URL}")

# Test the health endpoint first to make sure the server is running
try:
    health_response = requests.get(f"{API_URL}/health", timeout=10)
    print(f"Health check - Status Code: {health_response.status_code}")
    if health_response.status_code == 200:
        print("✓ Backend server is running")
    else:
        print(f"✗ Backend server issue: {health_response.text}")
except Exception as e:
    print(f"✗ Cannot reach backend server: {e}")
    print("Make sure your backend server is running on the expected port!")
    exit()

# Test the auth endpoint to see if we can get a test user
print("\nTrying to authenticate a test user...")

# Try to login with a known user (user ID 1)
login_data = {
    "email": "direct_test_4cec2811@example.com",
    "password": "testpassword123"  # This is likely not the real password
}

try:
    login_response = requests.post(f"{API_URL}/api/auth/login", json=login_data, timeout=10)
    print(f"Login attempt - Status Code: {login_response.status_code}")
    if login_response.status_code == 200:
        token_data = login_response.json()
        access_token = token_data.get('access_token')
        print("✓ Login successful")
    else:
        print(f"✗ Login failed: {login_response.text}")
        print("Will try to test with a dummy token to check the endpoint structure")
        access_token = "dummy_token_for_testing"
except Exception as e:
    print(f"Login request error: {e}")
    access_token = "dummy_token_for_testing"

# Test the tasks endpoint with the token
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

try:
    tasks_response = requests.get(f"{API_URL}/api/tasks", headers=headers, timeout=10)
    print(f"\nTasks endpoint - Status Code: {tasks_response.status_code}")
    print(f"Response: {tasks_response.text[:1000]}...")  # First 1000 chars
    
    # Try to parse as JSON
    try:
        json_data = tasks_response.json()
        print(f"\nParsed as JSON, type: {type(json_data)}")
        if isinstance(json_data, list):
            print(f"✓ Got an array with {len(json_data)} tasks")
            for i, task in enumerate(json_data[:3]):  # Show first 3 tasks
                print(f"  Task {i+1}: {task}")
        else:
            print(f"Got non-array response: {json_data}")
    except Exception as e:
        print(f"Could not parse response as JSON: {e}")
        
except Exception as e:
    print(f"Error making tasks request: {e}")