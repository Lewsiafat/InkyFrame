"""Configuration settings for the Inky Photo Display application."""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).parent.parent

# Upload settings
UPLOAD_DIR = BASE_DIR / "uploads"
ORIGINALS_DIR = UPLOAD_DIR / "originals"
OPTIMIZED_DIR = UPLOAD_DIR / "optimized"
THUMBNAILS_DIR = UPLOAD_DIR / "thumbnails"

# File upload constraints
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "bmp", "webp"}

# Display settings
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 480
DEFAULT_SATURATION = 0.5

# Weather settings
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
WEATHER_LOCATION = os.getenv("WEATHER_LOCATION", "Taipei,TW")
WEATHER_UNITS = os.getenv("WEATHER_UNITS", "metric")  # metric or imperial
WEATHER_CACHE_MINUTES = int(os.getenv("WEATHER_CACHE_MINUTES", "30"))

# Thumbnail settings
THUMBNAIL_WIDTH = 200
THUMBNAIL_HEIGHT = 120

# Server settings
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))

# Inky display model (auto-detect by default)
INKY_MODEL = os.getenv("INKY_MODEL", "auto")

# Ensure directories exist
ORIGINALS_DIR.mkdir(parents=True, exist_ok=True)
OPTIMIZED_DIR.mkdir(parents=True, exist_ok=True)
THUMBNAILS_DIR.mkdir(parents=True, exist_ok=True)
