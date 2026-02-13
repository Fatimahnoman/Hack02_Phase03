import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get the API URL
API_URL = os.getenv('NEXT_PUBLIC_API_URL', 'http://127.0.0.1:8000')
print(f"Testing API at: {API_URL}")

# Test the tasks endpoint
try:
    response = requests.get(f"{API_URL}/api/tasks", timeout=10)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text[:500]}...")  # First 500 chars
    
    # Try to parse as JSON
    try:
        json_data = response.json()
        print(f"Parsed as JSON, type: {type(json_data)}")
        print(f"Length if array: {len(json_data) if isinstance(json_data, list) else 'N/A'}")
    except:
        print("Could not parse response as JSON")
        
except Exception as e:
    print(f"Error making request: {e}")
    print("Make sure your backend server is running!")