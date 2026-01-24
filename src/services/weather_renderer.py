"""Weather renderer for creating e-ink display images."""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import logging

from src.config import DISPLAY_WIDTH, DISPLAY_HEIGHT, OPTIMIZED_DIR
from src.models.weather import WeatherCurrent, WeatherForecast

logger = logging.getLogger(__name__)

# Weather icon text mapping (using text instead of emoji for better compatibility)
WEATHER_ICONS = {
    "01d": "CLEAR",      # clear sky day
    "01n": "CLEAR",      # clear sky night
    "02d": "PARTLY",     # few clouds day
    "02n": "CLOUDY",     # few clouds night
    "03d": "CLOUDY",     # scattered clouds
    "03n": "CLOUDY",
    "04d": "CLOUDY",     # broken clouds
    "04n": "CLOUDY",
    "09d": "RAIN",       # shower rain
    "09n": "RAIN",
    "10d": "RAIN",       # rain day
    "10n": "RAIN",       # rain night
    "11d": "STORM",      # thunderstorm
    "11n": "STORM",
    "13d": "SNOW",       # snow
    "13n": "SNOW",
    "50d": "MIST",       # mist
    "50n": "MIST",
}


class WeatherRenderer:
    """Renderer for creating weather display images for e-ink."""
    
    def __init__(self):
        """Initialize weather renderer."""
        self.width = DISPLAY_WIDTH
        self.height = DISPLAY_HEIGHT
        self._load_fonts()
    
    def _load_fonts(self):
        """Load fonts with fallback to default."""
        try:
            # Try to load DejaVu fonts (commonly available on Linux)
            self.title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
            self.location_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)
            self.temp_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
            self.label_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
            self.forecast_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
            self.day_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
            self.icon_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
            logger.info("Loaded DejaVu fonts successfully")
        except:
            try:
                # Fallback to Liberation fonts
                self.title_font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", 36)
                self.location_font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", 28)
                self.temp_font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", 60)
                self.label_font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", 20)
                self.forecast_font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", 18)
                self.day_font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", 16)
                self.icon_font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", 24)
                logger.info("Loaded Liberation fonts successfully")
            except:
                # Final fallback to default font
                logger.warning("Could not load TrueType fonts, using default")
                self.title_font = ImageFont.load_default()
                self.location_font = ImageFont.load_default()
                self.temp_font = ImageFont.load_default()
                self.label_font = ImageFont.load_default()
                self.forecast_font = ImageFont.load_default()
                self.day_font = ImageFont.load_default()
                self.icon_font = ImageFont.load_default()
    
    def _get_weather_icon(self, icon_code: str) -> str:
        """Get text representation for weather icon code."""
        return WEATHER_ICONS.get(icon_code, "CLEAR")
    
    def render_weather(
        self,
        current: WeatherCurrent,
        forecast: WeatherForecast,
        output_filename: str = "weather_display"
    ) -> Path:
        """
        Render weather display image for e-ink.
        
        Args:
            current: Current weather data
            forecast: 5-day forecast data
            output_filename: Output filename (without extension)
            
        Returns:
            Path to generated image
        """
        # Create white background
        img = Image.new('RGB', (self.width, self.height), 'white')
        draw = ImageDraw.Draw(img)
        
        y_pos = 20
        
        # Location (no title, start with location)
        draw.text((30, y_pos), current.location, font=self.location_font, fill='black')
        y_pos += 45
        
        # Current temperature and icon
        temp_text = f"{int(current.temperature)}°C"
        draw.text((30, y_pos), temp_text, font=self.temp_font, fill='black')
        
        # Weather icon as text
        icon_text = self._get_weather_icon(current.icon)
        draw.text((220, y_pos + 10), icon_text, font=self.icon_font, fill='black')
        y_pos += 75
        
        # Weather description
        draw.text((30, y_pos), current.description, font=self.location_font, fill='black')
        y_pos += 40
        
        # Details
        details = [
            f"Feels like: {int(current.feels_like)}°C",
            f"Humidity: {current.humidity}%",
            f"Wind: {current.wind_speed} m/s"
        ]
        
        for detail in details:
            draw.text((30, y_pos), detail, font=self.label_font, fill='black')
            y_pos += 28
        
        # Separator line
        y_pos += 10
        draw.line([(30, y_pos), (self.width - 30, y_pos)], fill='black', width=2)
        y_pos += 15
        
        # 5-Day Forecast Title
        draw.text((30, y_pos), "5-DAY FORECAST", font=self.title_font, fill='black')
        y_pos += 45
        
        # Forecast cards
        card_width = (self.width - 80) // 5
        x_start = 30
        
        for i, day in enumerate(forecast.days[:5]):
            x_pos = x_start + (i * card_width)
            card_y = y_pos
            
            # Day name
            draw.text((x_pos + 5, card_y), day.day_name, font=self.day_font, fill='black')
            card_y += 25
            
            # Weather icon as text
            day_icon = self._get_weather_icon(day.icon)
            draw.text((x_pos + 5, card_y), day_icon, font=self.forecast_font, fill='black')
            card_y += 30
            
            # High temp
            draw.text((x_pos + 5, card_y), f"H: {int(day.temp_high)}°", font=self.forecast_font, fill='black')
            card_y += 25
            
            # Low temp
            draw.text((x_pos + 5, card_y), f"L: {int(day.temp_low)}°", font=self.forecast_font, fill='gray')
            
            # Vertical separator (except for last card)
            if i < 4:
                line_x = x_pos + card_width - 5
                draw.line([(line_x, y_pos), (line_x, y_pos + 100)], fill='lightgray', width=1)
        
        # Timestamp at bottom - use ASCII only to avoid encoding issues
        year = current.timestamp.year
        month = current.timestamp.month
        day = current.timestamp.day
        hour = current.timestamp.hour
        minute = current.timestamp.minute
        timestamp_text = f"Updated: {year}-{month:02d}-{day:02d} {hour:02d}:{minute:02d}"
        draw.text((30, self.height - 40), timestamp_text, font=self.label_font, fill='gray')
        
        # Save image
        output_path = OPTIMIZED_DIR / f"{output_filename}.jpg"
        img.save(output_path, 'JPEG', quality=95)
        
        logger.info(f"Weather display image saved to {output_path}")
        return output_path


# Global weather renderer instance
weather_renderer = WeatherRenderer()
