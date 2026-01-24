"""Weather service for fetching data from OpenWeatherMap API."""
import httpx
from datetime import datetime, timedelta
from typing import Optional
import logging
from dateutil import parser

from src.config import (
    OPENWEATHER_API_KEY,
    WEATHER_LOCATION,
    WEATHER_UNITS,
    WEATHER_CACHE_MINUTES
)
from src.models.weather import WeatherCurrent, ForecastDay, WeatherForecast

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# OpenWeatherMap API endpoints
CURRENT_WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"


class WeatherCache:
    """Simple in-memory cache for weather data."""
    
    def __init__(self):
        self._current_cache = {}
        self._forecast_cache = {}
    
    def get_current(self, location: str) -> Optional[WeatherCurrent]:
        """Get cached current weather."""
        if location in self._current_cache:
            data, timestamp = self._current_cache[location]
            if datetime.now() - timestamp < timedelta(minutes=WEATHER_CACHE_MINUTES):
                return data
        return None
    
    def set_current(self, location: str, data: WeatherCurrent):
        """Cache current weather."""
        self._current_cache[location] = (data, datetime.now())
    
    def get_forecast(self, location: str) -> Optional[WeatherForecast]:
        """Get cached forecast."""
        if location in self._forecast_cache:
            data, timestamp = self._forecast_cache[location]
            if datetime.now() - timestamp < timedelta(minutes=WEATHER_CACHE_MINUTES):
                return data
        return None
    
    def set_forecast(self, location: str, data: WeatherForecast):
        """Cache forecast."""
        self._forecast_cache[location] = (data, datetime.now())


class WeatherService:
    """Service for fetching weather data from OpenWeatherMap."""
    
    def __init__(self):
        """Initialize weather service."""
        self.cache = WeatherCache()
        self.api_key = OPENWEATHER_API_KEY
    
    def _check_api_key(self):
        """Check if API key is configured."""
        if not self.api_key:
            raise ValueError("OpenWeatherMap API key not configured. Set OPENWEATHER_API_KEY environment variable.")
    
    async def get_current_weather(self, location: Optional[str] = None) -> WeatherCurrent:
        """
        Fetch current weather for a location.
        
        Args:
            location: City name (defaults to configured location)
            
        Returns:
            WeatherCurrent object
            
        Raises:
            ValueError: If API key not configured
            httpx.HTTPError: If API request fails
        """
        self._check_api_key()
        location = location or WEATHER_LOCATION
        
        # Check cache first
        cached = self.cache.get_current(location)
        if cached:
            logger.info(f"Returning cached current weather for {location}")
            return cached
        
        # Fetch from API
        logger.info(f"Fetching current weather for {location} from OpenWeatherMap")
        
        params = {
            "q": location,
            "appid": self.api_key,
            "units": WEATHER_UNITS
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(CURRENT_WEATHER_URL, params=params)
            response.raise_for_status()
            data = response.json()
        
        # Parse response
        weather = WeatherCurrent(
            temperature=data["main"]["temp"],
            feels_like=data["main"]["feels_like"],
            humidity=data["main"]["humidity"],
            description=data["weather"][0]["description"].capitalize(),
            icon=data["weather"][0]["icon"],
            wind_speed=data["wind"]["speed"],
            location=data["name"],
            timestamp=datetime.now()
        )
        
        # Cache result
        self.cache.set_current(location, weather)
        
        return weather
    
    async def get_forecast(self, location: Optional[str] = None) -> WeatherForecast:
        """
        Fetch 5-day forecast for a location.
        
        Args:
            location: City name (defaults to configured location)
            
        Returns:
            WeatherForecast object
            
        Raises:
            ValueError: If API key not configured
            httpx.HTTPError: If API request fails
        """
        self._check_api_key()
        location = location or WEATHER_LOCATION
        
        # Check cache first
        cached = self.cache.get_forecast(location)
        if cached:
            logger.info(f"Returning cached forecast for {location}")
            return cached
        
        # Fetch from API
        logger.info(f"Fetching forecast for {location} from OpenWeatherMap")
        
        params = {
            "q": location,
            "appid": self.api_key,
            "units": WEATHER_UNITS
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(FORECAST_URL, params=params)
            response.raise_for_status()
            data = response.json()
        
        # Parse response - group by day and get daily highs/lows
        daily_data = {}
        
        for item in data["list"]:
            dt = parser.parse(item["dt_txt"])
            date_key = dt.date()
            
            if date_key not in daily_data:
                daily_data[date_key] = {
                    "temps": [],
                    "descriptions": [],
                    "icons": [],
                    "precipitation": []
                }
            
            daily_data[date_key]["temps"].append(item["main"]["temp"])
            daily_data[date_key]["descriptions"].append(item["weather"][0]["description"])
            daily_data[date_key]["icons"].append(item["weather"][0]["icon"])
            
            # Get precipitation probability if available
            if "pop" in item:
                daily_data[date_key]["precipitation"].append(item["pop"] * 100)
        
        # Create forecast days (limit to 5 days)
        forecast_days = []
        for date_key in sorted(daily_data.keys())[:5]:
            day_data = daily_data[date_key]
            
            forecast_day = ForecastDay(
                date=str(date_key),
                day_name=date_key.strftime("%a"),
                temp_high=max(day_data["temps"]),
                temp_low=min(day_data["temps"]),
                description=max(set(day_data["descriptions"]), key=day_data["descriptions"].count).capitalize(),
                icon=max(set(day_data["icons"]), key=day_data["icons"].count),
                precipitation=sum(day_data["precipitation"]) / len(day_data["precipitation"]) if day_data["precipitation"] else 0
            )
            forecast_days.append(forecast_day)
        
        forecast = WeatherForecast(
            location=data["city"]["name"],
            days=forecast_days
        )
        
        # Cache result
        self.cache.set_forecast(location, forecast)
        
        return forecast


# Global weather service instance
weather_service = WeatherService()
