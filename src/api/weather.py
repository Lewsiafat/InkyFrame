"""Weather API endpoints."""
from fastapi import APIRouter, HTTPException, status, BackgroundTasks
from typing import Optional

from src.models.weather import (
    WeatherCurrent,
    WeatherForecast,
    WeatherDisplayRequest,
    WeatherConfig
)
from src.models.photo import DisplayResponse, DisplayStatus
from src.services.weather_service import weather_service
from src.services.display_controller import display_controller
from src.config import (
    OPENWEATHER_API_KEY,
    WEATHER_LOCATION,
    WEATHER_UNITS,
    WEATHER_CACHE_MINUTES
)

router = APIRouter(prefix="/api/weather", tags=["weather"])


@router.get("/current", response_model=WeatherCurrent)
async def get_current_weather(location: Optional[str] = None):
    """
    Get current weather for a location.
    
    Args:
        location: City name (optional, uses default if not provided)
        
    Returns:
        Current weather data
        
    Raises:
        HTTPException: If API key not configured or request fails
    """
    try:
        weather = await weather_service.get_current_weather(location)
        return weather
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch weather: {str(e)}"
        )


@router.get("/forecast", response_model=WeatherForecast)
async def get_forecast(location: Optional[str] = None):
    """
    Get 5-day forecast for a location.
    
    Args:
        location: City name (optional, uses default if not provided)
        
    Returns:
        5-day forecast data
        
    Raises:
        HTTPException: If API key not configured or request fails
    """
    try:
        forecast = await weather_service.get_forecast(location)
        return forecast
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch forecast: {str(e)}"
        )


@router.post("/display", response_model=DisplayResponse, status_code=status.HTTP_202_ACCEPTED)
async def display_weather(
    request: WeatherDisplayRequest = WeatherDisplayRequest(),
    background_tasks: BackgroundTasks = None
):
    """
    Display weather on the Inky e-ink display.
    
    Args:
        request: Display request with optional location
        background_tasks: FastAPI background tasks
        
    Returns:
        Display response with status
        
    Raises:
        HTTPException: If display busy or weather fetch fails
    """
    # Check if display is already updating
    if display_controller.status == DisplayStatus.UPDATING:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Display update already in progress"
        )
    
    try:
        # Import weather renderer
        from src.services.weather_renderer import weather_renderer
        
        # Fetch weather data
        current = await weather_service.get_current_weather(request.location)
        forecast = await weather_service.get_forecast(request.location)
        
        # Render weather image
        image_path = weather_renderer.render_weather(current, forecast)
        
        # Display on Inky in background
        background_tasks.add_task(
            display_controller.display_photo,
            image_path,
            "weather_display"
        )
        
        return DisplayResponse(
            status=DisplayStatus.UPDATING,
            estimated_time=25,
            message=f"Weather display started for {current.location}"
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to display weather: {str(e)}"
        )


@router.get("/config", response_model=WeatherConfig)
async def get_weather_config():
    """
    Get weather configuration.
    
    Returns:
        Weather configuration
    """
    return WeatherConfig(
        api_key_configured=bool(OPENWEATHER_API_KEY),
        location=WEATHER_LOCATION,
        units=WEATHER_UNITS,
        cache_minutes=WEATHER_CACHE_MINUTES
    )
