"""
Pydantic schemas for request validation and response serialization.

Schemas ensure that incoming data conforms to expected formats and that
responses are serialized consistently. They also provide OpenAPI
documentation automatically when used with FastAPI.
"""

from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import List, Optional


class WeatherDay(BaseModel):
    """Representation of forecast data for a single day."""

    date: str
    temp_max_c: Optional[float] = None
    temp_min_c: Optional[float] = None
    precipitation_mm: Optional[float] = None
    weathercode: Optional[int] = None


class WeatherResponse(BaseModel):
    """Response model for a weekly weather forecast."""

    latitude: float
    longitude: float
    start_date: str
    end_date: str
    days: List[WeatherDay]


class SignUpRequest(BaseModel):
    """Request payload for user signup."""

    email: EmailStr
    password: str = Field(min_length=8, description="Password must be at least 8 characters long")


class LoginRequest(BaseModel):
    """Request payload for user login."""

    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Response model for authentication, containing an access token."""

    access_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    """
    Response model exposing user information.

    The `created_at` field has been removed from this model to align with the
    simplified `User` database model, which no longer includes a timestamp
    column. If you choose to add a `created_at` field back into the database,
    you can reintroduce it here as well.
    """

    id: int
    email: EmailStr

    class Config:
        orm_mode = True