import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from dotenv import load_dotenv
from services.agent_service import AgentService
from core.database import get_session_context
from models.user import User
from sqlmodel import select
from datetime import datetime, timezone
import asyncio

# Load environment variables
load_dotenv()

def test_agent_service():
    print("Testing Agent Service with new API key...")
    
    # Get a database session
    with get_session_context() as session:
        # Get or create a default user
        user = session.exec(select(User).limit(1)).first()
        if not user:
            # Create a default user if none exists
            from services.auth_service import get_password_hash
            import secrets
            
            default_email = "test@example.com"
            default_password = secrets.token_urlsafe(32)
            hashed_password = get_password_hash(default_password)
            current_time = datetime.now(timezone.utc)

            user = User(
                email=default_email,
                hashed_password=hashed_password,
                created_at=current_time,
                updated_at=current_time
            )
            
            session.add(user)
            session.commit()
            session.refresh(user)
        
        print(f"Using user ID: {user.id}")
        
        # Create the agent service
        agent_service = AgentService(session, user.id)
        
        # Test the process_request method directly
        try:
            result = agent_service.process_request(
                user_input="Hello, how are you?",
                conversation_history=[]
            )
            print(f"Success! Result: {result}")
        except Exception as e:
            print(f"Error in agent service: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_agent_service()