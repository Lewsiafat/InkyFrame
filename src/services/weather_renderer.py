"""Weather renderer for creating e-ink display images."""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import logging

from src.config import DISPLAY_WIDTH, DISPLAY_HEIGHT, OPTIMIZED_DIR
from src.models.weather import WeatherCurrent, WeatherForecast

logger = logging.getLogger(__name__)

# Weather icon emoji mapping
WEATHER_ICONS = {
    "01d": "☀️",  # clear sky day
    "01n": "🌙",  # clear sky night
    "02d": "⛅",  # few clouds day
    "02n": "☁️",  # few clouds night
    "03d": "☁️",  # scattered clouds
    "03n": "☁️",
    "04d": "☁️",  # broken clouds
    "04n": "☁️",
    "09d": "🌧️",  # shower rain
    "09n": "🌧️",
    "10d": "🌦️",  # rain day
    "10n": "🌧️",  # rain night
    "11d": "⛈️",  # thunderstorm
    "11n": "⛈️",
    "13d": "❄️",  # snow
    "13n": "❄️",
    "50d": "🌫️",  # mist
    "50n": "🌫️",
}


class WeatherRenderer:
    """Renderer for creating weather display images for e-ink."""
    
    def __init__(self):
        """Initialize weather renderer."""
        self.width = DISPLAY_WIDTH
        self.height = DISPLAY_HEIGHT
    
    def _get_weather_icon(self, icon_code: str) -> str:
        """Get emoji for weather icon code."""
        return WEATHER_ICONS.get(icon_code, "🌤️")
    
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
        
        # Try to use a nice font, fall back to default if not available
        try:
            title_font = ImageFont.truetype("arial.ttf", 48)
            location_font = ImageFont.truetype("arial.ttf", 36)
            temp_font = ImageFont.truetype("arialbd.ttf", 72)
            label_font = ImageFont.truetype("arial.ttf", 24)
            forecast_font = ImageFont.truetype("arial.ttf", 20)
            day_font = ImageFont.truetype("arialbd.ttf", 18)
        except:
            # Fallback to default font
            title_font = ImageFont.load_default()
            location_font = ImageFont.load_default()
            temp_font = ImageFont.load_default()
            label_font = ImageFont.load_default()
            forecast_font = ImageFont.load_default()
            day_font = ImageFont.load_default()
        
        y_pos = 20
        
        # Title
        draw.text((40, y_pos), "CURRENT WEATHER", font=title_font, fill='black')
        y_pos += 70
        
        # Location
        draw.text((40, y_pos), current.location, font=location_font, fill='black')
        y_pos += 60
        
        # Current temperature (large)
        temp_text = f"{int(current.temperature)}°C"
        draw.text((40, y_pos), temp_text, font=temp_font, fill='black')
        
        # Weather icon (emoji as text)
        icon = self._get_weather_icon(current.icon)
        draw.text((250, y_pos), icon, font=temp_font, fill='black')
        y_pos += 90
        
        # Weather description
        draw.text((40, y_pos), current.description, font=location_font, fill='black')
        y_pos += 50
        
        # Details
        details = [
            f"Feels like: {int(current.feels_like)}°C",
            f"Humidity: {current.humidity}%",
            f"Wind: {current.wind_speed} m/s"
        ]
        
        for detail in details:
            draw.text((40, y_pos), detail, font=label_font, fill='black')
            y_pos += 35
        
        # Separator line
        y_pos += 10
        draw.line([(40, y_pos), (self.width - 40, y_pos)], fill='black', width=2)
        y_pos += 20
        
        # 5-Day Forecast Title
        draw.text((40, y_pos), "5-DAY FORECAST", font=title_font, fill='black')
        y_pos += 60
        
        # Forecast cards
        card_width = (self.width - 120) // 5
        x_start = 40
        
        for i, day in enumerate(forecast.days[:5]):
            x_pos = x_start + (i * card_width)
            card_y = y_pos
            
            # Day name
            draw.text((x_pos + 10, card_y), day.day_name, font=day_font, fill='black')
            card_y += 30
            
            # Weather icon
            day_icon = self._get_weather_icon(day.icon)
            draw.text((x_pos + 10, card_y), day_icon, font=location_font, fill='black')
            card_y += 50
            
            # High temp
            draw.text((x_pos + 10, card_y), f"{int(day.temp_high)}°", font=forecast_font, fill='black')
            card_y += 28
            
            # Low temp
            draw.text((x_pos + 10, card_y), f"{int(day.temp_low)}°", font=forecast_font, fill='gray')
            
            # Vertical separator (except for last card)
            if i < 4:
                line_x = x_pos + card_width - 5
                draw.line([(line_x, y_pos), (line_x, y_pos + 130)], fill='lightgray', width=1)
        
        # Timestamp at bottom
        timestamp_text = f"Updated: {current.timestamp.strftime('%Y-%m-%d %H:%M')}"
        draw.text((40, self.height - 40), timestamp_text, font=label_font, fill='gray')
        
        # Save image
        output_path = OPTIMIZED_DIR / f"{output_filename}.jpg"
        img.save(output_path, 'JPEG', quality=95)
        
        logger.info(f"Weather display image saved to {output_path}")
        return output_path


# Global weather renderer instance
weather_renderer = WeatherRenderer()
