#!/usr/bin/env python3
"""
Test script to check OpenRouter account status
"""

import requests

def check_account_status(api_key):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Try to access account info endpoint
    try:
        response = requests.get("https://openrouter.ai/api/v1/account", headers=headers)
        print(f"Account endpoint status: {response.status_code}")
        print(f"Account endpoint response text: {response.text}")
        if response.status_code == 200:
            try:
                print(f"Account info: {response.json()}")
            except:
                print("Could not parse JSON response for account info")
        else:
            print(f"Account endpoint response: {response.text}")
    except Exception as e:
        print(f"Error checking account status: {e}")
    
    # Try to access rate limits
    try:
        response = requests.get("https://openrouter.ai/api/v1/rate-limits", headers=headers)
        print(f"Rate limits endpoint status: {response.status_code}")
        print(f"Rate limits response text: {response.text}")
        if response.status_code == 200:
            try:
                print(f"Rate limits: {response.json()}")
            except:
                print("Could not parse JSON response for rate limits")
        else:
            print(f"Rate limits endpoint response: {response.text}")
    except Exception as e:
        print(f"Error checking rate limits: {e}")

if __name__ == "__main__":
    api_key = "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"
    check_account_status(api_key)