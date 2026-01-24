# InkyFrame

> 📸🌤️ A FastAPI web server for displaying photos and weather on Pimoroni Inky Impression e-ink displays

A web-based application that allows users to upload photos, view weather forecasts, and display them on an Inky Impression 7.3" e-ink display. Features automatic image optimization for e-ink's unique 6-color Spectra palette and real-time weather data from OpenWeatherMap.

---

## Features

### Photo Display
- 📤 **Photo Upload**: Drag-and-drop or click-to-browse file upload
- 🖼️ **Photo Gallery**: Grid view of all uploaded photos with thumbnails
- 🎨 **Automatic Optimization**: Images automatically resized and optimized for e-ink
- 🎯 **6-Color Quantization**: Converts images to Inky's Spectra 6 palette
- 📱 **Responsive Design**: Works on desktop and mobile browsers

### Weather Display
- 🌤️ **Current Weather**: Real-time weather conditions with temperature, humidity, wind
- 📅 **5-Day Forecast**: Daily forecast with high/low temperatures
- 🌍 **Location Support**: Configure any city worldwide
- 🔄 **Auto-Caching**: 30-minute cache to reduce API calls
- 📊 **E-ink Optimized**: Clean black & white layout perfect for e-ink displays

### General
- ⚡ **Real-time Status**: Live display status updates
- 🔀 **Tab Navigation**: Easy switching between Photos and Weather views
- 🎯 **One-Click Display**: Send photos or weather to e-ink with one button

## Quick Start

### Prerequisites

- Python 3.11+
- Raspberry Pi (or compatible SBC) with Inky Impression 7.3" display
- `uv` package manager
- OpenWeatherMap API key (free tier available)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Lewsiafat/InkyFrame.git
cd InkyFrame
```

2. Install dependencies:
```bash
uv sync
```

3. Configure environment variables (create `.env` file):
```env
OPENWEATHER_API_KEY=your_api_key_here
WEATHER_LOCATION=Taipei,TW
WEATHER_UNITS=metric
WEATHER_CACHE_MINUTES=30
```

4. Run the development server:
```bash
uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

5. Open your browser and navigate to:
```
http://localhost:8000
```

## Deployment

### Quick Deploy to Development Board

Use the simple deployment script to upload code to your server:

```cmd
deploy_simple.bat
```

Then SSH into your server and restart:

```bash
ssh YOUR_USERNAME@YOUR_SERVER_IP
cd /path/to/InkyFrame
pkill -f uvicorn
uv run uvicorn src.main:app --host 0.0.0.0 --port 8000
```

**For detailed deployment instructions, see:**
- [SERVER_INSTALL.md](SERVER_INSTALL.md) - Server setup guide
- [DEPLOYMENT.md](DEPLOYMENT.md) - Full deployment documentation
- [INSTALL_INKY.md](INSTALL_INKY.md) - Inky library installation

## Usage

### Photo Display
1. Click the **📸 Photos** tab
2. **Upload Photos**: Drag and drop photos onto the upload area
3. **View Gallery**: Browse all uploaded photos
4. **Display Photo**: Click a photo to preview, then "Display on Inky"
5. **Delete Photos**: Use the delete button in the preview modal

### Weather Display
1. Click the **🌤️ Weather** tab
2. View current weather and 5-day forecast for your configured location
3. Click **"Display Weather on Inky"** to send to e-ink display
4. Weather updates automatically (cached for 30 minutes)

## Project Structure

```
InkyFrame/
├── src/
│   ├── api/              # API endpoints
│   │   ├── upload.py     # Photo upload
│   │   ├── gallery.py    # Gallery management
│   │   ├── display.py    # Display control
│   │   └── weather.py    # Weather endpoints
│   ├── services/         # Business logic
│   │   ├── storage.py    # File storage
│   │   ├── image_processor.py      # Image optimization
│   │   ├── display_controller.py   # Inky display control
│   │   ├── weather_service.py      # OpenWeatherMap API
│   │   └── weather_renderer.py     # Weather image generation
│   ├── models/           # Data models
│   │   ├── photo.py      # Photo models
│   │   └── weather.py    # Weather models
│   ├── config.py         # Configuration
│   └── main.py           # FastAPI application
├── static/               # Frontend files
│   ├── css/
│   │   └── style.css     # Styles
│   ├── js/
│   │   └── app.js        # Frontend logic
│   └── index.html        # Main page
├── uploads/              # Uploaded files (auto-created)
│   ├── originals/        # Original uploads
│   ├── optimized/        # Inky-optimized versions
│   └── thumbnails/       # Gallery thumbnails
├── spec/                 # Documentation
│   └── project_spec.md   # Project specification
├── deploy_simple.bat     # Simple deployment script
└── pyproject.toml        # Dependencies
```

## API Endpoints

### Photo Management
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Web interface |
| POST | `/api/upload` | Upload photo |
| GET | `/api/photos` | List all photos |
| GET | `/api/photos/{id}` | Get photo details |
| DELETE | `/api/photos/{id}` | Delete photo |
| POST | `/api/display/{id}` | Display photo on Inky |
| GET | `/api/status` | Get display status |

### Weather
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/weather/current` | Get current weather |
| GET | `/api/weather/forecast` | Get 5-day forecast |
| POST | `/api/weather/display` | Display weather on Inky |
| GET | `/api/weather/config` | Get weather configuration |

### System
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/docs` | API documentation (Swagger) |
| GET | `/redoc` | API documentation (ReDoc) |

## Configuration

### Environment Variables

**Server:**
- `HOST`: Server host (default: `0.0.0.0`)
- `PORT`: Server port (default: `8000`)

**Display:**
- `INKY_MODEL`: Display model (default: `auto`)
- `DISPLAY_WIDTH`: Display width (default: `800`)
- `DISPLAY_HEIGHT`: Display height (default: `480`)

**Upload:**
- `MAX_FILE_SIZE`: Max upload size in bytes (default: `10485760` = 10MB)
- `ALLOWED_EXTENSIONS`: Allowed file types (default: `jpg,jpeg,png,bmp,webp`)

**Weather:**
- `OPENWEATHER_API_KEY`: Your OpenWeatherMap API key (required for weather)
- `WEATHER_LOCATION`: Default location (default: `Taipei,TW`)
- `WEATHER_UNITS`: Units system - `metric` or `imperial` (default: `metric`)
- `WEATHER_CACHE_MINUTES`: Cache duration in minutes (default: `30`)

### Getting OpenWeatherMap API Key

1. Sign up at: https://openweathermap.org/api
2. Navigate to: https://home.openweathermap.org/api_keys
3. Copy your API key
4. Add to `.env` file or set as environment variable

Free tier includes:
- 1,000 API calls per day
- Current weather data
- 5-day forecast
- Global coverage

## Image Processing

The application automatically:

1. Resizes images to 800×480 pixels (maintaining aspect ratio)
2. Applies letterboxing if needed
3. Quantizes to 6-color Spectra palette (Black, White, Yellow, Red, Blue, Green)
4. Applies Floyd-Steinberg dithering for smooth gradients
5. Generates thumbnails for the gallery

## Weather Rendering

Weather displays include:

1. **Current Weather**: Location, temperature, weather icon, description
2. **Details**: Feels-like temperature, humidity, wind speed
3. **5-Day Forecast**: Daily cards with day name, weather icon, high/low temps
4. **Timestamp**: Last update time (right-aligned)
5. **E-ink Optimization**: Black & white layout with text-based weather icons

## Development

### Running Tests

```bash
uv run pytest tests/
```

### Production Deployment

```bash
uv run uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 2
```

### Mock Mode

If the Inky library is not available (e.g., running on non-Raspberry Pi), the application runs in mock mode, simulating display updates without actual hardware.

## Supported Image Formats

- JPEG (.jpg, .jpeg)
- PNG (.png)
- BMP (.bmp)
- WebP (.webp)

## Technologies

- **Backend**: FastAPI, Python 3.11+
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **Image Processing**: Pillow (PIL)
- **E-ink Display**: Pimoroni Inky Impression 7.3"
- **Weather API**: OpenWeatherMap
- **HTTP Client**: httpx (async)
- **Package Manager**: uv

## License

MIT License - See LICENSE file for details.

## Documentation

- [Server Installation Guide](SERVER_INSTALL.md)
- [Deployment Guide](DEPLOYMENT.md)
- [Inky Library Installation](INSTALL_INKY.md)
- [Weather Testing Guide](WEATHER_TESTING.md)
- [Project Specification](spec/project_spec.md)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- [Pimoroni](https://shop.pimoroni.com/) for the Inky Impression display
- [OpenWeatherMap](https://openweathermap.org/) for weather data API
- [FastAPI](https://fastapi.tiangolo.com/) for the excellent web framework
