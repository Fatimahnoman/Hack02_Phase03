import sys
sys.path.insert(0, 'backend')
from backend.src.core.database import get_session_context
from backend.src.models.user import User
from sqlmodel import select

session_gen = get_session_context()
session = next(session_gen)

try:
    users = session.exec(select(User)).all()
    print('Users in database:')
    for user in users:
        print(f'ID: {user.id}, Email: {user.email}')
finally:
    next(session_gen)