from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlmodel import Session
from typing import Optional
from datetime import timedelta
from pydantic import BaseModel
from ..core.database import get_session_context
from ..models.user import User, UserCreate, UserRead
from ..services.auth_service import (
    authenticate_user,
    create_user,
    create_access_token,
    get_user_by_email
)

router = APIRouter()
security = HTTPBearer()

@router.post("/register", response_model=UserRead)
def register(user: UserCreate, session: Session = Depends(get_session_context)):
    try:
        # Check if user already exists
        existing_user = get_user_by_email(session, user.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Create new user
        db_user = create_user(session, user)
        return db_user
    except HTTPException:
        # Re-raise HTTP exceptions as-is to preserve the intended behavior
        raise
    except Exception as e:
        print(f"Registration error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/login")
def login(request: LoginRequest, session: Session = Depends(get_session_context)):
    user = authenticate_user(session, request.email, request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}