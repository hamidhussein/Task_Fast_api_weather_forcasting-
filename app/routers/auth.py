from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from ..schemas import SignUpRequest, LoginRequest, TokenResponse
from ..utils.auth import hash_password, verify_password, create_access_token, oauth2_scheme
from ..database import get_db
from ..models import User


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=TokenResponse)
async def signup(request: SignUpRequest, db: Session = Depends(get_db)):
    """
    Register a new user and return an access token.
    """
    # Check if the email is already registered
    existing_user = db.query(User).filter(User.email == request.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )
    # Create user with hashed password
    new_user = User(email=request.email, password_hash=hash_password(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    # Create access token
    access_token = create_access_token(subject=str(new_user.id))
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Authenticate a user and return an access token.
    """
    # OAuth2PasswordRequestForm provides fields `username` and `password`
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    access_token = create_access_token(subject=str(user.id))
    return {"access_token": access_token, "token_type": "bearer"}