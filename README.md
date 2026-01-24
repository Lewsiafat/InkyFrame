# Inky Photo Display Web Server

A FastAPI-based web application for uploading photos and displaying them on an Inky Impression 7.3" e-ink display.

## Features

- 📤 **Photo Upload**: Drag-and-drop or click-to-browse file upload
- 🖼️ **Photo Gallery**: Grid view of all uploaded photos with thumbnails
- 🎨 **Automatic Optimization**: Images are automatically resized and optimized for the e-ink display
- 🎯 **6-Color Quantization**: Converts images to Inky's Spectra 6 color palette
- 📱 **Responsive Design**: Works on desktop and mobile browsers
- ⚡ **Real-time Status**: Live display status updates

## Quick Start

### Prerequisites

- Python 3.11+
- Raspberry Pi (or compatible SBC) with Inky Impression 7.3" display
- `uv` package manager

### Installation

1. Clone the repository:
```bash
cd inky
```

2. Install dependencies:
```bash
uv sync
```

3. Run the development server:
```bash
uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

4. Open your browser and navigate to:
```
http://localhost:8000
```

## Usage

1. **Upload Photos**: Drag and drop photos onto the upload area or click to browse
2. **View Gallery**: Browse all uploaded photos in the gallery
3. **Display Photo**: Click on a photo to preview, then click "Display on Inky" to send it to the e-ink display
4. **Delete Photos**: Click on a photo and use the delete button to remove it

## Project Structure

```
inky/
├── src/
│   ├── api/              # API endpoints
│   │   ├── upload.py     # Photo upload
│   │   ├── gallery.py    # Gallery management
│   │   └── display.py    # Display control
│   ├── services/         # Business logic
│   │   ├── storage.py    # File storage
│   │   ├── image_processor.py  # Image optimization
│   │   └── display_controller.py  # Inky display control
│   ├── models/           # Data models
│   │   └── photo.py      # Pydantic models
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
│   ├── inky_api_spec.md  # API specification
│   ├── inky_impression_73_hardware_spec.md  # Hardware spec
│   └── project_spec.md   # Project specification
└── pyproject.toml        # Dependencies

```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Web interface |
| POST | `/api/upload` | Upload photo |
| GET | `/api/photos` | List all photos |
| GET | `/api/photos/{id}` | Get photo details |
| DELETE | `/api/photos/{id}` | Delete photo |
| POST | `/api/display/{id}` | Display photo on Inky |
| GET | `/api/status` | Get display status |
| GET | `/health` | Health check |

## Configuration

Environment variables:

- `HOST`: Server host (default: `0.0.0.0`)
- `PORT`: Server port (default: `8000`)
- `INKY_MODEL`: Display model (default: `auto`)
- `MAX_FILE_SIZE`: Max upload size in bytes (default: `10485760` = 10MB)

## Image Processing

The application automatically:

1. Resizes images to 800×480 pixels (maintaining aspect ratio)
2. Applies letterboxing if needed
3. Quantizes to 6-color Spectra palette (Black, White, Yellow, Red, Blue, Green)
4. Applies Floyd-Steinberg dithering for smooth gradients
5. Generates thumbnails for the gallery

## Development

### Running Tests

```bash
uv run pytest tests/
```

### Production Deployment

```bash
uv run uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 2
```

## Mock Mode

If the Inky library is not available (e.g., running on non-Raspberry Pi), the application runs in mock mode, simulating display updates without actual hardware.

## Supported Image Formats

- JPEG (.jpg, .jpeg)
- PNG (.png)
- BMP (.bmp)
- WebP (.webp)

## License

See LICENSE file for details.

## Documentation

- [API Specification](spec/inky_api_spec.md)
- [Hardware Specification](spec/inky_impression_73_hardware_spec.md)
- [Project Specification](spec/project_spec.md)
