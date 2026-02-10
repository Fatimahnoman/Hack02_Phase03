#!/usr/bin/env python3
"""
Test script to verify Cohere API connectivity
"""

import requests
import json

def test_cohere_api():
    api_key = "TQwvkd2x0ZnCBAi2yYW0NL8lW4v14dBN11InjN0w"
    url = "https://api.cohere.ai/v1/chat"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "command-r-plus",
        "message": "Hello, how are you?",
        "max_tokens": 50
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        print(f"Cohere API response status: {response.status_code}")
        if response.status_code == 200:
            response_data = response.json()
            print("Cohere API test successful!")
            print(f"Response: {response_data.get('text', 'No text in response')}")
            return True
        else:
            print(f"Cohere API error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"Error testing Cohere API: {e}")
        return False

if __name__ == "__main__":
    test_cohere_api()