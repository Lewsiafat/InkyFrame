# Inky Photo Display Web Server - Project Specification

**Version:** 1.0  
**Date:** 2026-01-24  
**Target Display:** Inky Impression 7.3" (800×480, Spectra 6)

---

## Project Overview

A web-based application that allows users to upload photos via a browser interface, select images from a gallery, and display them on an Inky Impression e-ink display. The backend automatically optimizes images for the e-ink display's unique color palette and resolution.

---

## Core Features

### 1. Photo Upload
- **Web Interface:** Drag-and-drop or click-to-browse file upload
- **Supported Formats:** JPEG, PNG, BMP, WebP
- **File Size Limit:** 10MB maximum
- **Validation:** Server-side file type and size validation
- **Storage:** Persistent storage of original images

### 2. Photo Gallery
- **Grid View:** Thumbnail gallery of all uploaded photos
- **Metadata Display:** Filename, upload date, file size
- **Actions:** View, select for display, delete
- **Responsive Design:** Works on desktop and mobile browsers

### 3. Photo Selection & Display
- **Preview:** Full-size preview before sending to display
- **Display Control:** One-click button to send to Inky
- **Status Feedback:** Real-time display status (idle, updating, complete, error)
- **Estimated Time:** Show expected refresh time (~20-25 seconds)

### 4. Image Optimization
- **Automatic Resizing:** Scale to 800×480 pixels
- **Aspect Ratio:** Maintain original aspect ratio with letterboxing
- **Color Quantization:** Convert to 6-color Spectra palette
- **Dithering:** Floyd-Steinberg dithering for smooth gradients
- **Saturation Control:** Adjustable saturation (default: 0.5)
- **Caching:** Store optimized versions to avoid reprocessing

---

## Technical Stack

### Backend
- **Framework:** FastAPI (Python 3.11+)
- **ASGI Server:** Uvicorn
- **Image Processing:** Pillow (PIL)
- **Display Driver:** Inky library (Pimoroni)
- **Validation:** Pydantic
- **Async I/O:** aiofiles

### Frontend
- **HTML5:** Semantic markup
- **CSS3:** Modern responsive design
- **JavaScript:** Vanilla JS (no framework dependencies)
- **API Communication:** Fetch API

### Infrastructure
- **Package Manager:** uv
- **Python Version:** 3.11+
- **Platform:** Raspberry Pi (or compatible SBC with GPIO)

---

## System Architecture

```
┌─────────────┐
│   Browser   │
│   (Client)  │
└──────┬──────┘
       │ HTTP/REST API
       ▼
┌─────────────────────────────┐
│     FastAPI Server          │
│  ┌─────────────────────┐    │
│  │  Upload Handler     │    │
│  │  Gallery Manager    │    │
│  │  Display Controller │    │
│  └─────────────────────┘    │
└──────┬──────────────┬───────┘
       │              │
       ▼              ▼
┌──────────────┐  ┌──────────────┐
│ Image        │  │ Inky Display │
│ Processor    │  │ Driver       │
└──────┬───────┘  └──────┬───────┘
       │                 │
       ▼                 ▼
┌──────────────┐  ┌──────────────┐
│ File Storage │  │ E-ink Panel  │
│ (uploads/)   │  │ (Hardware)   │
└──────────────┘  └──────────────┘
```

---

## API Specification

### Endpoints

#### Upload Photo
```http
POST /api/upload
Content-Type: multipart/form-data

Request Body:
- file: <image file>

Response: 200 OK
{
  "id": "uuid-string",
  "filename": "photo.jpg",
  "size": 1234567,
  "timestamp": "2026-01-24T13:27:00Z"
}
```

#### List Photos
```http
GET /api/photos

Response: 200 OK
{
  "photos": [
    {
      "id": "uuid-string",
      "filename": "photo.jpg",
      "size": 1234567,
      "timestamp": "2026-01-24T13:27:00Z",
      "thumbnail_url": "/api/photos/uuid-string/thumbnail"
    }
  ]
}
```

#### Get Photo Details
```http
GET /api/photos/{photo_id}

Response: 200 OK
{
  "id": "uuid-string",
  "filename": "photo.jpg",
  "size": 1234567,
  "timestamp": "2026-01-24T13:27:00Z",
  "original_url": "/uploads/originals/uuid-string.jpg",
  "optimized_url": "/uploads/optimized/uuid-string.jpg"
}
```

#### Delete Photo
```http
DELETE /api/photos/{photo_id}

Response: 204 No Content
```

#### Display Photo
```http
POST /api/display/{photo_id}
Content-Type: application/json

Request Body (optional):
{
  "saturation": 0.5
}

Response: 202 Accepted
{
  "status": "updating",
  "estimated_time": 25,
  "message": "Display update started"
}
```

#### Get Display Status
```http
GET /api/status

Response: 200 OK
{
  "status": "idle",  // idle | updating | error
  "current_photo_id": "uuid-string",
  "last_update": "2026-01-24T13:27:00Z"
}
```

---

## Image Processing Pipeline

### Step 1: Load Original
- Read uploaded image file
- Validate image format

### Step 2: Resize
- Calculate target dimensions maintaining aspect ratio
- Resize using high-quality resampling (Lanczos)

### Step 3: Letterbox (if needed)
- Add white/black bars to reach exact 800×480
- Center image in frame

### Step 4: Color Quantization
- Convert to RGB mode
- Apply Inky's 6-color palette
- Blend saturation between desaturated and saturated palettes

### Step 5: Dithering
- Apply Floyd-Steinberg dithering
- Smooth color transitions

### Step 6: Save Optimized
- Save to `uploads/optimized/` directory
- Generate thumbnail (200×120) for gallery

---

## File Storage Structure

```
uploads/
├── originals/              # Original uploaded files
│   ├── {uuid}.jpg
│   ├── {uuid}.png
│   └── ...
├── optimized/              # Inky-optimized versions (800×480)
│   ├── {uuid}.jpg
│   └── ...
└── thumbnails/             # Gallery thumbnails (200×120)
    ├── {uuid}.jpg
    └── ...
```

---

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `UPLOAD_DIR` | `./uploads` | Upload directory path |
| `MAX_FILE_SIZE` | `10485760` | Max file size (10MB) |
| `ALLOWED_EXTENSIONS` | `jpg,jpeg,png,bmp,webp` | Allowed file types |
| `DEFAULT_SATURATION` | `0.5` | Default saturation level |
| `INKY_MODEL` | `auto` | Display model (auto-detect) |
| `HOST` | `0.0.0.0` | Server host |
| `PORT` | `8000` | Server port |

---

## Display Integration

### Inky Display Configuration
- **Model:** Auto-detect via EEPROM or manual specification
- **Resolution:** 800×480 pixels
- **Colors:** 6 colors (Black, White, Yellow, Red, Blue, Green)
- **Refresh Time:** ~20-25 seconds
- **Busy Wait:** Monitor BUSY pin for completion

### Error Handling
- **Timeout:** 30-second maximum for display update
- **Retry Logic:** Up to 3 retries on failure
- **Status Tracking:** Maintain display state (idle/updating/error)
- **Logging:** Record all display operations

---

## Security Considerations

### File Upload Security
- ✅ Validate file types by content (magic bytes)
- ✅ Limit file sizes (10MB max)
- ✅ Sanitize filenames (use UUID)
- ✅ Prevent path traversal attacks
- ✅ Validate image integrity

### API Security
- ✅ CORS configuration
- ✅ Rate limiting on uploads
- ✅ Input validation with Pydantic
- ✅ Error message sanitization

---

## Performance Requirements

### Response Times
- **Upload:** < 2 seconds for 5MB file
- **Gallery Load:** < 1 second for 100 photos
- **Image Optimization:** < 3 seconds per image
- **Display Update:** 20-25 seconds (hardware limitation)

### Scalability
- **Concurrent Uploads:** Support 5 simultaneous uploads
- **Storage:** Handle 1000+ photos
- **Memory:** < 512MB RAM usage

---

## User Interface Design

### Upload Section
- Large dropzone with drag-and-drop
- File browser fallback
- Upload progress bar
- Success/error notifications

### Gallery Section
- Responsive grid layout (3-5 columns)
- Thumbnail images with metadata
- Hover effects for interactivity
- Delete confirmation dialog

### Display Controls
- "Display on Inky" button
- Status indicator (idle/updating/error)
- Progress feedback during update
- Success confirmation

---

## Development Workflow

### Setup
```bash
# Install dependencies
uv sync

# Run development server
uv run uvicorn src.main:app --reload
```

### Testing
```bash
# Run unit tests
uv run pytest tests/

# Run with coverage
uv run pytest --cov=src tests/
```

### Deployment
```bash
# Production server
uv run uvicorn src.main:app --host 0.0.0.0 --port 8000
```

---

## Future Enhancements (Out of Scope)

- 🔮 User authentication and multi-user support
- 🔮 Photo albums/collections
- 🔮 Advanced image filters and effects
- 🔮 Multi-display support
- 🔮 Cloud storage integration (S3, etc.)
- 🔮 Mobile app (iOS/Android)
- 🔮 WebSocket for real-time status updates

---

## Success Criteria

### Functional Requirements
- ✅ Users can upload photos via web interface
- ✅ Gallery displays all uploaded photos
- ✅ Selected photos display correctly on Inky
- ✅ Images are automatically optimized for e-ink
- ✅ Display status is visible to users

### Non-Functional Requirements
- ✅ Upload completes within 2 seconds
- ✅ Image optimization completes within 3 seconds
- ✅ UI is responsive on mobile and desktop
- ✅ System handles errors gracefully
- ✅ Code is well-documented and maintainable

---

## Dependencies

### Python Packages
```toml
[project.dependencies]
fastapi = "^0.109.0"
uvicorn = {extras = ["standard"], version = "^0.27.0"}
python-multipart = "^0.0.9"
pillow = "^10.2.0"
pydantic = "^2.5.0"
aiofiles = "^23.2.1"
inky = "^2.2.1"
```

---

## Glossary

- **E-ink:** Electronic ink display technology using electrophoresis
- **Spectra 6:** 6-color e-ink technology by E Ink Corporation
- **Quantization:** Process of reducing color palette to limited set
- **Dithering:** Technique to simulate colors using available palette
- **Letterboxing:** Adding bars to maintain aspect ratio
- **ASGI:** Asynchronous Server Gateway Interface
- **UUID:** Universally Unique Identifier

---

*This specification serves as the blueprint for developing the Inky Photo Display Web Server. All implementation should align with these requirements.*
