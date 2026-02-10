#!/usr/bin/env python3
"""
Test script to verify JWT token creation and validation.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.src.services.auth_service import create_access_token, verify_token
from backend.src.core.config import settings
from datetime import timedelta
import jwt as pyjwt

def test_jwt_functionality():
    print("Testing JWT token creation and validation...")
    print(f"Algorithm: {settings.algorithm}")
    print(f"Secret key length: {len(settings.secret_key)}")
    
    # Test token creation
    test_data = {"sub": "test@example.com"}
    token = create_access_token(data=test_data, expires_delta=timedelta(minutes=30))
    print(f"Token created: {token[:50]}...")
    
    # Test token verification
    decoded_payload = verify_token(token)
    print(f"Token verification result: {decoded_payload}")
    
    # Test direct JWT decoding to compare
    try:
        direct_decode = pyjwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        print(f"Direct JWT decode result: {direct_decode}")
    except Exception as e:
        print(f"Direct JWT decode error: {e}")
    
    # Test with malformed token
    try:
        bad_payload = verify_token("invalid.token.here")
        print(f"Invalid token result: {bad_payload}")
    except Exception as e:
        print(f"Invalid token error: {e}")
    
    # Test with wrong secret key
    try:
        wrong_secret_token = pyjwt.encode(test_data, "wrong_secret", algorithm=settings.algorithm)
        wrong_payload = verify_token(wrong_secret_token)
        print(f"Wrong secret result: {wrong_payload}")
    except Exception as e:
        print(f"Wrong secret error: {e}")

if __name__ == "__main__":
    test_jwt_functionality()