import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get the API key and other settings
api_key = os.getenv("OPENROUTER_API_KEY")
base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
model = os.getenv("OPENROUTER_MODEL", "openai/gpt-3.5-turbo")

print(f"Testing OpenRouter API connection...")

# Prepare the request payload
payload = {
    "model": model,
    "messages": [
        {
            "role": "user",
            "content": "Hello, how are you?"
        }
    ],
    "temperature": 0.7,
    "max_tokens": 100
}

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

try:
    # Make the API request
    response = requests.post(
        f"{base_url}/chat/completions",
        headers=headers,
        json=payload
    )

    print(f"Response Status Code: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")
    
    if response.status_code == 200:
        response_data = response.json()
        print(f"Success! Response: {response_data['choices'][0]['message']['content']}")
    else:
        print(f"Error: {response.status_code}")
        print(f"Response Text: {response.text}")
        
except Exception as e:
    print(f"Exception occurred: {str(e)}")