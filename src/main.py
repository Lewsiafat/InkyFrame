"""Main FastAPI application for Inky Photo Display."""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pathlib import Path

from src.api import upload, gallery, display, weather
from src.config import BASE_DIR, UPLOAD_DIR

# Create FastAPI app
app = FastAPI(
    title="InkyFrame",
    description="Web server for uploading and displaying photos on Inky e-ink displays",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(upload.router)
app.include_router(gallery.router)
app.include_router(display.router)
app.include_router(weather.router)

# Mount static files
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
app.mount("/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")


@app.get("/")
async def root():
    """Serve the main web interface."""
    return FileResponse(str(BASE_DIR / "static" / "index.html"))


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    from src.config import HOST, PORT
    
    uvicorn.run(
        "src.main:app",
        host=HOST,
        port=PORT,
        reload=True
    )
