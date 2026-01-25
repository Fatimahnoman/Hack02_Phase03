from sqlmodel import Session, select
from fastapi import HTTPException, status, Depends, Security
from typing import Optional
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from ..models.user import User, UserCreate, UserRead
from ..config import settings
from ..database import get_session

# Password hashing
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# Create JWT token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt

# Verify password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Hash password
def get_password_hash(password: str) -> str:
    try:
        return pwd_context.hash(password)
    except Exception as e:
        error_msg = str(e)
        # Handle bcrypt's 72-byte password limit specifically
        if "password cannot be longer than 72 bytes" in error_msg or "truncate manually if necessary" in error_msg:
            raise ValueError("Password must not exceed 72 characters for security reasons")
        else:
            # Re-raise other hashing errors with more context
            raise ValueError(f"Password hashing failed: {error_msg}")

# Get user by email
def get_user_by_email(session: Session, email: str) -> Optional[User]:
    statement = select(User).where(User.email == email)
    user = session.exec(statement).first()
    return user

# Authenticate user
def authenticate_user(session: Session, email: str, password: str) -> Optional[User]:
    user = get_user_by_email(session, email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

# Create user
def create_user(session: Session, user_create: UserCreate) -> UserRead:
    hashed_password = get_password_hash(user_create.password)
    current_time = datetime.now(timezone.utc)
    db_user = User(
        email=user_create.email,
        hashed_password=hashed_password,
        created_at=current_time,
        updated_at=current_time
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    # Return a UserRead object without sensitive data
    return UserRead(
        id=db_user.id,
        email=db_user.email,
        created_at=db_user.created_at,
        updated_at=db_user.updated_at
    )

# Verify token
def verify_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        email: str = payload.get("sub")
        if email is None:
            return None
        return payload
    except JWTError:
        return None

from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

# Get current user from token
def get_current_user_from_token(session: Session, token: str) -> Optional[UserRead]:
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    email = payload.get("sub")
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = get_user_by_email(session, email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


# FastAPI dependency to get current user from Bearer token
security = HTTPBearer()

def get_current_user(
    session: Session = Depends(get_session),
    credentials: HTTPAuthorizationCredentials = Security(security)
) -> UserRead:
    token = credentials.credentials
    return get_current_user_from_token(session, token)