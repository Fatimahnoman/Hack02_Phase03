import requests
import json
import time

# Wait a moment to ensure server is ready
time.sleep(2)

# Test the health endpoint first
try:
    print("Testing health endpoint...")
    health_response = requests.get('http://127.0.0.1:8000/health', timeout=10)
    print(f'Health check: {health_response.status_code}')
    print(f'Response: {health_response.json()}')
except Exception as e:
    print(f'Health check failed: {e}')

# Test the login endpoint
login_data = {
    'email': 'fatimah.noman@gmail.com',
    'password': 'TestPassword123!'
}

try:
    print("\nTesting login endpoint...")
    login_response = requests.post('http://127.0.0.1:8000/api/auth/login', json=login_data, timeout=15)
    print(f'Login status: {login_response.status_code}')
    print(f'Login response: {login_response.text}')

    if login_response.status_code == 200:
        print("SUCCESS: Login was successful!")
        response_data = login_response.json()
        if 'access_token' in response_data:
            print(f"Access token received: {response_data['access_token'][:50]}...")
    elif login_response.status_code == 401:
        print("FAILURE: Login failed - incorrect email or password")
    else:
        print(f"UNEXPECTED STATUS CODE: {login_response.status_code}")

except requests.exceptions.Timeout:
    print('Login request timed out')
except requests.exceptions.ConnectionError:
    print('Could not connect to the server')
except Exception as e:
    print(f'Login request failed with error: {e}')