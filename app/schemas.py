from pydantic import BaseModel, EmailStr, Field
from typing import List


class WeatherDay(BaseModel):
    date: str
    temp_max_c: float
    temp_min_c: float
    precipitation_mm: float
    weathercode: int


class WeatherResponse(BaseModel):
    latitude: float
    longitude: float
    start_date: str
    end_date: str
    days: List[WeatherDay]


class SignUpRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"