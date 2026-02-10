#!/usr/bin/env python3
"""
Test script to check if OpenAI API configuration is working properly.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.src.core.config import settings
import cohere

def test_cohere_config():
    print("Testing Cohere API configuration...")
    print(f"API Key: {'*' * 20}{settings.cohere_api_key[-5:] if settings.cohere_api_key else 'NOT SET'}")
    print(f"Model: {settings.cohere_model}")
    
    if not settings.cohere_api_key:
        print("[ERROR] COHERE_API_KEY is not set!")
        return False
    
    try:
        client = cohere.Client(api_key=settings.cohere_api_key)
        response = client.chat(message="Hello, are you working?", model=settings.cohere_model, max_tokens=10)
        print(f"[SUCCESS] Cohere API is working. Response: {response.text[:50]}...")
        return True
    except Exception as e:
        print(f"[ERROR] Cohere API test failed: {e}")
        return False

if __name__ == "__main__":
    test_cohere_config()