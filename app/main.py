from fastapi import FastAPI
from .routers import auth as auth_router
from .routers import weather as weather_router


app = FastAPI(title="Weather Forecasting App", version="1.0.0")

# Include the auth and weather routers
app.include_router(auth_router.router)
app.include_router(weather_router.router)


@app.get("/", tags=["meta"])
def root():
    """Health check endpoint."""
    return {"name": "Weather Forecasting App", "status": "ok"}