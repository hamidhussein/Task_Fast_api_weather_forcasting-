from fastapi import APIRouter, Depends, Query, HTTPException
from ..utils.auth import get_current_user
from ..schemas import WeatherResponse, WeatherDay
from ..config import settings
import httpx


router = APIRouter(prefix="/weather", tags=["weather"])


@router.get("", response_model=WeatherResponse)
async def get_week_forecast(
    city: str = Query(..., description="City name for the weather forecast"),
    lat: float = Query(..., ge=-90, le=90, description="Latitude"),
    lon: float = Query(..., ge=-180, le=180, description="Longitude"),
    current_user=Depends(get_current_user),
):
    """
    Retrieve a 7‑day weather forecast for the specified city.
    Requires an authenticated user.
    """
    base_url = "https://api.weatherapi.com/v1/forecast.json"
    params = {
        "key": settings.weather_api_key,
        "q": city,
        "days": 7,
        "aqi": "no",
        "alerts": "no",
    }
    async with httpx.AsyncClient(timeout=20) as client:
        response = await client.get(base_url, params=params)
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            # Convert HTTP errors to FastAPI HTTPException
            raise HTTPException(
                status_code=exc.response.status_code, detail=str(exc)
            ) from exc
        data = response.json()

    if "error" in data:
        raise HTTPException(status_code=404, detail=data["error"]["message"])

    forecast = data.get("forecast", {}).get("forecastday", [])
    if not forecast:
        raise HTTPException(
            status_code=404,
            detail="No forecast data available for the specified location.",
        )

    days = []
    for day in forecast:
        days.append(
            WeatherDay(
                date=day["date"],
                temp_max_c=day["day"]["maxtemp_c"],
                temp_min_c=day["day"]["mintemp_c"],
                precipitation_mm=day["day"]["totalprecip_mm"],
                weathercode=day["day"]["condition"]["code"],
            )
        )

    return WeatherResponse(
        latitude=data["location"]["lat"],
        longitude=data["location"]["lon"],
        start_date=forecast[0]["date"],
        end_date=forecast[-1]["date"],
        days=days,
    )