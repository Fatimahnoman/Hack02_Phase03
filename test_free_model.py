#!/usr/bin/env python3
"""
Test script to verify OpenRouter API connectivity with a known free model
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

import cohere
from backend.src.core.config import settings

def test_free_model():
    print("Testing Cohere API with model...")
    print(f"API Key configured: {bool(settings.cohere_api_key)}")
    print(f"Model: {settings.cohere_model}")

    if not settings.cohere_api_key:
        print("ERROR: No COHERE_API_KEY configured!")
        return False

    client = cohere.Client(api_key=settings.cohere_api_key)

    try:
        print(f"Attempting to call model: {settings.cohere_model}")
        response = client.chat(message="Hello, are you working? Just say 'Yes' if you are.", model=settings.cohere_model, max_tokens=10)
        
        print("✅ Cohere API connection successful!")
        print(f"Response: {response.text}")
        return True

    except Exception as e:
        print(f"❌ Cohere API connection failed: {e}")
        print(f"Error type: {type(e).__name__}")
        return False

if __name__ == "__main__":
    test_free_model()