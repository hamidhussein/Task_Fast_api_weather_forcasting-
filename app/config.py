"""
Configuration management for the Weather Forecasting API.

This module defines Pydantic-based models to load configuration
from a JSON file. The configuration includes database credentials,
JWT parameters and the API key for the weather service.
The values are loaded at import time by calling `load_settings()`.  
Editing `config.json` allows you to change settings without
modifying the code.
"""

import json
from pathlib import Path
from pydantic import BaseModel


class DBSettings(BaseModel):
    """Settings related to the PostgreSQL database."""
    database_user: str
    database_password: str
    database_host: str
    database_port: int
    database_name: str

    @property
    def sqlalchemy_url(self) -> str:
        """Assemble the full SQLAlchemy URL for PostgreSQL."""
        return (
            f"postgresql+psycopg2://{self.database_user}:{self.database_password}"  
            f"@{self.database_host}:{self.database_port}/{self.database_name}"
        )


class JWTSettings(BaseModel):
    """Settings for JSON Web Token (JWT) authentication."""
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60


class WeatherAPISettings(BaseModel):
    """Settings for the external WeatherAPI service."""
    api_key: str


class Settings(BaseModel):
    """Top-level configuration object grouping all settings."""
    database: DBSettings
    jwt: JWTSettings
    weather_api: WeatherAPISettings


def load_settings(
    config_path: str | Path = Path(__file__).resolve().parents[1] / "config.json",
) -> Settings:
    """Load configuration from a JSON file and return a Settings object.

    The default path points to a `config.json` file in the project root.
    """
    data = json.loads(Path(config_path).read_text())
    return Settings(**data)


# Load settings at import time.  
# This makes `settings` available throughout the application.
settings = load_settings()