"""Weather data models for the Inky Photo Display application."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class WeatherCurrent(BaseModel):
    """Current weather conditions."""
    temperature: float = Field(..., description="Current temperature")
    feels_like: float = Field(..., description="Feels like temperature")
    humidity: int = Field(..., description="Humidity percentage")
    description: str = Field(..., description="Weather description")
    icon: str = Field(..., description="Weather icon code")
    wind_speed: float = Field(..., description="Wind speed")
    location: str = Field(..., description="Location name")
    timestamp: datetime = Field(default_factory=datetime.now, description="Data timestamp")
    
    class Config:
        json_schema_extra = {
            "example": {
                "temperature": 25.5,
                "feels_like": 23.2,
                "humidity": 65,
                "description": "Partly cloudy",
                "icon": "02d",
                "wind_speed": 12.5,
                "location": "Hong Kong",
                "timestamp": "2026-01-24T19:14:00Z"
            }
        }


class ForecastDay(BaseModel):
    """Single day forecast."""
    date: str = Field(..., description="Date (YYYY-MM-DD)")
    day_name: str = Field(..., description="Day name (Mon, Tue, etc)")
    temp_high: float = Field(..., description="High temperature")
    temp_low: float = Field(..., description="Low temperature")
    description: str = Field(..., description="Weather description")
    icon: str = Field(..., description="Weather icon code")
    precipitation: float = Field(default=0.0, description="Precipitation probability (0-100)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "date": "2026-01-25",
                "day_name": "Sat",
                "temp_high": 28.0,
                "temp_low": 18.0,
                "description": "Sunny",
                "icon": "01d",
                "precipitation": 10.0
            }
        }


class WeatherForecast(BaseModel):
    """5-day weather forecast."""
    location: str = Field(..., description="Location name")
    days: list[ForecastDay] = Field(..., description="List of forecast days")
    
    class Config:
        json_schema_extra = {
            "example": {
                "location": "Hong Kong",
                "days": []
            }
        }


class WeatherDisplayRequest(BaseModel):
    """Weather display request."""
    location: Optional[str] = Field(None, description="Location (uses default if not provided)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "location": "Hong Kong"
            }
        }


class WeatherConfig(BaseModel):
    """Weather configuration."""
    api_key_configured: bool = Field(..., description="Whether API key is configured")
    location: str = Field(..., description="Default location")
    units: str = Field(..., description="Temperature units (metric/imperial)")
    cache_minutes: int = Field(..., description="Cache duration in minutes")
    
    class Config:
        json_schema_extra = {
            "example": {
                "api_key_configured": True,
                "location": "Hong Kong",
                "units": "metric",
                "cache_minutes": 30
            }
        }
