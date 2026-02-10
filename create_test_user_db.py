import sys
sys.path.insert(0, 'backend')
from backend.src.core.database import get_session_context
from backend.src.models.user import User
from backend.src.services.auth_service import create_user, get_password_hash
from backend.src.models.user import UserCreate

session_gen = get_session_context()
session = next(session_gen)

try:
    # Create a test user with a known password
    test_email = "testuser@example.com"
    test_password = "TestPassword123!"
    
    # Check if user already exists
    from sqlmodel import select
    existing_user = session.exec(select(User).where(User.email == test_email)).first()
    
    if existing_user:
        print(f"User {test_email} already exists")
        user_id = existing_user.id
    else:
        # Create new user
        user_create = UserCreate(email=test_email, password=test_password)
        created_user = create_user(session, user_create)
        user_id = created_user.id
        print(f"Created user {test_email} with ID {user_id}")
    
    print(f"Test user ID: {user_id}")
    
finally:
    next(session_gen)