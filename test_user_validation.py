#!/usr/bin/env python3
"""
Test script to check if the user validation works properly with Neon database.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.src.services.stateless_conversation_service import StatelessConversationService
from backend.src.services.database_service import DatabaseService
from backend.src.core.database import get_session_context
import asyncio

async def test_user_validation():
    print("Testing user validation with Neon database...")
    
    # Create a session
    session_gen = get_session_context()
    session = next(session_gen)
    
    try:
        db_service = DatabaseService(session)
        service = StatelessConversationService(db_service)
        
        # Test the _validate_or_get_default_user_id method (this is now async)
        user_id = await service._validate_or_get_default_user_id(None)
        print(f'Default user_id resolved to: {user_id}')
        
        # Check if this user exists in the database
        from backend.src.models.user import User
        from sqlmodel import select
        user = session.exec(select(User).where(User.id == user_id)).first()
        print(f'User exists in DB: {user is not None}')
        if user:
            print(f'User email: {user.email}')
        
        # Test with a specific user_id
        user_id_1 = await service._validate_or_get_default_user_id('1')
        print(f'User ID 1 resolved to: {user_id_1}')
        user_1 = session.exec(select(User).where(User.id == 1)).first()
        print(f'User 1 exists in DB: {user_1 is not None}')
        if user_1:
            print(f'User 1 email: {user_1.email}')
        
        # Test with a non-existent user_id
        user_id_nonexistent = await service._validate_or_get_default_user_id('999')
        print(f'Non-existent user ID 999 resolved to: {user_id_nonexistent}')
        
        return True
        
    except Exception as e:
        print(f"Error in user validation test: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        next(session_gen)  # Close session

if __name__ == "__main__":
    success = asyncio.run(test_user_validation())
    if success:
        print("\nUser validation is working properly!")
    else:
        print("\nUser validation failed.")