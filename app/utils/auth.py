"""
Authentication utilities for the Weather Forecasting API.

This module provides helpers for hashing passwords, verifying hashes,
creating JWT tokens and retrieving the current user from a token.
It uses `passlib` for bcrypt hashing and `python-jose` for JWT handling.
"""

from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from ..config import settings
from ..database import get_db
from ..models import User


# Password hashing context using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# HTTP bearer scheme to extract the JWT token from the `Authorization` header.
# This informs Swagger/OpenAPI that the API uses a simple bearer token for authentication
# and shows a single field in the "Authorize" popup where users paste the JWT.
bearer_scheme = HTTPBearer()


def hash_password(password: str) -> str:
    """Hash a plaintext password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    """Verify a plaintext password against a stored bcrypt hash."""
    return pwd_context.verify(password, password_hash)


def create_access_token(subject: str) -> str:
    """Create a JWT token for the given subject (usually a user ID).

    The token includes an expiration timestamp based on the configuration.
    """
    expire = datetime.now(tz=timezone.utc) + timedelta(
        minutes=settings.jwt.access_token_expire_minutes
    )
    payload = {"sub": subject, "exp": expire}
    return jwt.encode(payload, settings.jwt.secret_key, algorithm=settings.jwt.algorithm)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    """
    Decode a JWT token from the Authorization header and return the corresponding user.

    Raises HTTPException if the token is invalid, expired, or the user cannot be found.
    """
    # The credentials object contains the scheme (e.g. "Bearer") and the token itself.
    token = credentials.credentials
    try:
        # Decode the JWT. If the token is invalid or expired, this will raise.
        payload = jwt.decode(
            token, settings.jwt.secret_key, algorithms=[settings.jwt.algorithm]
        )
        sub = payload.get("sub")
        if sub is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

    # Convert the subject to an integer user ID. In our model, IDs are integers.
    try:
        user_id = int(sub)
    except (TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload"
        )

    # Look up the user in the database
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )
    return user