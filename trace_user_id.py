import sys
import os
sys.path.insert(0, 'backend')

# Trace the user_id flow from chat to DB
from backend.src.services.stateless_conversation_service import StatelessConversationService
from backend.src.services.database_service import DatabaseService
from backend.src.core.database import get_session_context

# Create a session
session_gen = get_session_context()
session = next(session_gen)

try:
    db_service = DatabaseService(session)
    service = StatelessConversationService(db_service)
    
    # Check the _validate_or_get_default_user_id method
    user_id = service._validate_or_get_default_user_id(None)
    print(f'Default user_id resolved to: {user_id}')
    
    # Check if this user exists in the database
    from backend.src.models.user import User
    from sqlmodel import select
    user = session.exec(select(User).where(User.id == user_id)).first()
    print(f'User exists in DB: {user is not None}')
    if user:
        print(f'User email: {user.email}')
    
    # Test with a specific user_id
    user_id_1 = service._validate_or_get_default_user_id('1')
    print(f'User ID 1 resolved to: {user_id_1}')
    user_1 = session.exec(select(User).where(User.id == 1)).first()
    print(f'User 1 exists in DB: {user_1 is not None}')
    
finally:
    next(session_gen)  # Close session