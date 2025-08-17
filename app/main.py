"""
FastAPI application entry point for the Weather Forecasting API.

This module initializes the FastAPI app, includes authentication
and weather routers and exposes a simple root endpoint for
health checks. Importing this file in Uvicorn will start the
service.
"""

from fastapi import FastAPI
from .routers import auth as auth_router
from .routers import weather as weather_router


# Initialize the FastAPI app with metadata for OpenAPI docs
app = FastAPI(title="Weather Forecasting API", version="1.0.0")

# Register route modules.  Prefixes are defined in the routers.
app.include_router(auth_router.router)
app.include_router(weather_router.router)


@app.get("/", tags=["meta"])
def root():
    """Simple health check endpoint to verify the service is running."""
    return {"name": "Weather Forecasting API", "status": "ok"}