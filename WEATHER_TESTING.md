# Weather Display Feature - Testing Guide

## Setup

### 1. Get OpenWeatherMap API Key

1. Sign up at: https://openweathermap.org/api
2. Navigate to: https://home.openweathermap.org/api_keys
3. Copy your API key
4. Wait ~10 minutes for activation

### 2. Configure Environment

Create or update `.env` file in project root:

```env
OPENWEATHER_API_KEY=your_api_key_here
WEATHER_LOCATION=Hong Kong
WEATHER_UNITS=metric
WEATHER_CACHE_MINUTES=30
```

Or set environment variables:

**Windows (PowerShell):**
```powershell
$env:OPENWEATHER_API_KEY="your_api_key_here"
$env:WEATHER_LOCATION="Hong Kong"
```

**Linux/Mac:**
```bash
export OPENWEATHER_API_KEY="your_api_key_here"
export WEATHER_LOCATION="Hong Kong"
```

### 3. Start Server

```bash
uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

---

## Testing API Endpoints

### 1. Check Configuration

```bash
curl http://localhost:8000/api/weather/config
```

Expected response:
```json
{
  "api_key_configured": true,
  "location": "Hong Kong",
  "units": "metric",
  "cache_minutes": 30
}
```

### 2. Get Current Weather

```bash
curl http://localhost:8000/api/weather/current
```

Expected response:
```json
{
  "temperature": 25.5,
  "feels_like": 23.2,
  "humidity": 65,
  "description": "Partly cloudy",
  "icon": "02d",
  "wind_speed": 12.5,
  "location": "Hong Kong",
  "timestamp": "2026-01-24T19:14:00Z"
}
```

### 3. Get 5-Day Forecast

```bash
curl http://localhost:8000/api/weather/forecast
```

Expected response:
```json
{
  "location": "Hong Kong",
  "days": [
    {
      "date": "2026-01-25",
      "day_name": "Sat",
      "temp_high": 28.0,
      "temp_low": 18.0,
      "description": "Sunny",
      "icon": "01d",
      "precipitation": 10.0
    },
    // ... 4 more days
  ]
}
```

### 4. Test with Different Location

```bash
curl "http://localhost:8000/api/weather/current?location=London"
curl "http://localhost:8000/api/weather/forecast?location=Tokyo"
```

---

## API Documentation

Once server is running, visit:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

## Troubleshooting

### "API key not configured"

Make sure `OPENWEATHER_API_KEY` environment variable is set.

### "Invalid API key"

- Wait 10 minutes after creating the key
- Check if key is copied correctly
- Verify at: https://home.openweathermap.org/api_keys

### "City not found"

- Check spelling of city name
- Try with country code: "London,UK" or "New York,US"
- Use coordinates: `lat=22.3193&lon=114.1694` (for Hong Kong)

### Rate Limit Exceeded

Free tier allows 1,000 calls/day. Cache is enabled (30 minutes default) to reduce API calls.

---

## Next Steps

1. ✅ Backend API is complete
2. ⏳ Create weather renderer for e-ink display
3. ⏳ Add frontend UI for weather display
4. ⏳ Integrate with display controller

---

## Current Status

**Completed:**
- ✅ Weather data models
- ✅ OpenWeatherMap API integration
- ✅ Caching mechanism
- ✅ API endpoints (current, forecast, config)
- ✅ Error handling

**TODO:**
- ⏳ Weather renderer (create 800×480 image)
- ⏳ Frontend UI (weather section)
- ⏳ Display integration
- ⏳ Weather icons/graphics
