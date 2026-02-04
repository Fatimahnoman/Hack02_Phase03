import requests
import json
import time

# Wait a moment to ensure server is ready
time.sleep(2)

# Test the chat endpoint - don't include conversation_id if it's None
chat_data = {
    "message": "hi"
}
# conversation_id is optional, so we won't include it for a new conversation

try:
    print("Testing chat endpoint...")
    response = requests.post('http://127.0.0.1:8000/api/v1/chat', json=chat_data, timeout=30)
    print(f'Chat status: {response.status_code}')
    print(f'Chat response: {response.text}')

    if response.status_code == 200:
        print("SUCCESS: Chat is working!")
        response_data = response.json()
        if 'response' in response_data:
            print(f"Bot response: {response_data['response']}")
    else:
        print(f"FAILED: Chat failed with status code {response.status_code}")

except requests.exceptions.Timeout:
    print('Chat request timed out - this might be expected if the AI model is processing')
except requests.exceptions.ConnectionError:
    print('Could not connect to the server')
except Exception as e:
    print(f'Chat request failed with error: {e}')