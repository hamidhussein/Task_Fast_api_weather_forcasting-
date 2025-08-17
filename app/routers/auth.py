"""
Authentication routes for the Weather Forecasting API.

This module defines the FastAPI endpoints for user signup and login.
Upon successful authentication, users receive a JWT token which can be
used to access protected routes.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..schemas import SignUpRequest, LoginRequest, TokenResponse, UserOut
from ..utils.auth import hash_password, verify_password, create_access_token
from ..database import get_db
from ..models import User


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=TokenResponse)
async def signup(request: SignUpRequest, db: Session = Depends(get_db)):
    """Register a new user and return an access token."""
    # Check if the email is already registered
    existing_user = db.query(User).filter(User.email == request.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # Hash the password and create the user
    user = User(email=request.email, password_hash=hash_password(request.password))
    db.add(user)
    db.commit()
    db.refresh(user)

    # Create JWT token for the new user
    access_token = create_access_token(subject=str(user.id))

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    """Authenticate a user and return an access token."""
    # Find the user by email
    user = db.query(User).filter(User.email == request.email).first()
    # Verify credentials
    if not user or not verify_password(request.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    # Create JWT token for the authenticated user
    access_token = create_access_token(subject=str(user.id))
    return {"access_token": access_token, "token_type": "bearer"}