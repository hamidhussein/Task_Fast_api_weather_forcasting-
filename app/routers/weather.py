"""
Weather forecasting route for the Weather Forecasting API.

This module defines an endpoint that returns a seven‑day forecast for a given
city and date. The endpoint requires authentication via a JWT token.
Weather data is fetched from the external WeatherAPI service.  
See the WeatherAPI documentation for details on request parameters and
response fields: the base URL is `http://api.weatherapi.com/v1` and the
`forecast.json` method accepts a `q` parameter for the location and a `days`
parameter for the number of forecast days (1–14)【882191624372483†L100-L145】.
"""

from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, Query, HTTPException, status
import httpx
from ..utils.auth import get_current_user
from ..schemas import WeatherResponse, WeatherDay
from ..config import settings


router = APIRouter(prefix="/weather", tags=["weather"])


@router.get("", response_model=WeatherResponse)
async def get_week_forecast(
    date: str = Query(..., description="Start date in YYYY-MM-DD"),
    city: str = Query(..., description="City name for the weather forecast"),
    current_user=Depends(get_current_user),
):
    """
    Retrieve a 7‑day weather forecast for the specified city starting from the given date.

    The user must be authenticated via a JWT token. The function parses the date,
    calls the WeatherAPI forecast endpoint with the `days=7` parameter and
    returns a simplified forecast containing the date, max/min temperatures,
    total precipitation and weather code for each day.  
    WeatherAPI allows up to 14 days of forecast and requires a `days` parameter
    when using the forecast API【882191624372483†L139-L145】.
    """
    # Parse the provided date string
    try:
        start = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid date format. Use YYYY-MM-DD",
        )

    end = start + timedelta(days=6)

    # Compose the API request parameters
    base_url = "http://api.weatherapi.com/v1/forecast.json"
    params = {
        "key": settings.weather_api.api_key,
        "q": city,
        "days": 7,
        "aqi": "no",
        "alerts": "no",
    }

    # Fetch data asynchronously
    async with httpx.AsyncClient(timeout=20) as client:
        try:
            res = await client.get(base_url, params=params)
            res.raise_for_status()
        except httpx.HTTPStatusError as exc:
            # Convert HTTP errors to FastAPI exceptions
            raise HTTPException(
                status_code=exc.response.status_code,
                detail=str(exc),
            ) from exc
        data = res.json()

    # WeatherAPI returns an error object instead of forecast if the location is invalid
    if "error" in data:
        raise HTTPException(status_code=404, detail=data["error"].get("message"))

    # Extract forecast information
    forecast_days = data.get("forecast", {}).get("forecastday", [])
    if not forecast_days:
        raise HTTPException(
            status_code=404,
            detail="No forecast data available for the specified location.",
        )

    days: list[WeatherDay] = []
    for day in forecast_days:
        day_info = day.get("day", {})
        condition = day_info.get("condition", {})
        days.append(
            WeatherDay(
                date=day.get("date"),
                temp_max_c=day_info.get("maxtemp_c"),
                temp_min_c=day_info.get("mintemp_c"),
                precipitation_mm=day_info.get("totalprecip_mm"),
                weathercode=condition.get("code"),
            )
        )

    # Construct and return the response
    location = data.get("location", {})
    return WeatherResponse(
        latitude=location.get("lat", 0.0),
        longitude=location.get("lon", 0.0),
        start_date=start.isoformat(),
        end_date=end.isoformat(),
        days=days,
    )