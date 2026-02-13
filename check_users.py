import os
from dotenv import load_dotenv
from backend.src.core.database import engine
from backend.src.models.user import User
from sqlmodel import Session, select

# Load environment variables
load_dotenv()

def check_users():
    # Create a database session
    session = Session(engine)
    
    try:
        # Get all users
        all_users = session.exec(select(User)).all()
        
        print("All users in the database:")
        for i, user in enumerate(all_users):
            print(f"  {i+1}. ID: {user.id}, Email: {user.email}")
        
        # Check if there's a user with a common email you might be using
        common_emails = ['test@example.com', 'admin@example.com', 'user@example.com']
        for email in common_emails:
            user = session.exec(select(User).where(User.email == email)).first()
            if user:
                print(f"\nFound user with common email '{email}': ID {user.id}")
                
    finally:
        session.close()

if __name__ == "__main__":
    check_users()