"""Data models for the Inky Photo Display application."""
from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class DisplayStatus(str, Enum):
    """Display status enumeration."""
    IDLE = "idle"
    UPDATING = "updating"
    ERROR = "error"


class PhotoMetadata(BaseModel):
    """Photo metadata model."""
    id: str = Field(..., description="Unique photo identifier (UUID)")
    filename: str = Field(..., description="Original filename")
    size: int = Field(..., description="File size in bytes")
    timestamp: datetime = Field(default_factory=datetime.now, description="Upload timestamp")
    thumbnail_url: Optional[str] = Field(None, description="Thumbnail URL")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "filename": "sunset.jpg",
                "size": 1234567,
                "timestamp": "2026-01-24T13:42:00Z",
                "thumbnail_url": "/api/photos/550e8400-e29b-41d4-a716-446655440000/thumbnail"
            }
        }


class PhotoDetail(PhotoMetadata):
    """Detailed photo information."""
    original_url: str = Field(..., description="Original image URL")
    optimized_url: Optional[str] = Field(None, description="Optimized image URL")


class DisplayRequest(BaseModel):
    """Display request model."""
    saturation: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="Saturation level (0.0 = desaturated, 1.0 = saturated)"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "saturation": 0.5
            }
        }


class DisplayResponse(BaseModel):
    """Display response model."""
    status: DisplayStatus = Field(..., description="Current display status")
    estimated_time: int = Field(..., description="Estimated time in seconds")
    message: str = Field(..., description="Status message")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "updating",
                "estimated_time": 25,
                "message": "Display update started"
            }
        }


class StatusResponse(BaseModel):
    """Status response model."""
    status: DisplayStatus = Field(..., description="Current display status")
    current_photo_id: Optional[str] = Field(None, description="Currently displayed photo ID")
    last_update: Optional[datetime] = Field(None, description="Last update timestamp")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "idle",
                "current_photo_id": "550e8400-e29b-41d4-a716-446655440000",
                "last_update": "2026-01-24T13:42:00Z"
            }
        }


class PhotoListResponse(BaseModel):
    """Photo list response model."""
    photos: list[PhotoMetadata] = Field(..., description="List of photos")
    total: int = Field(..., description="Total number of photos")
    
    class Config:
        json_schema_extra = {
            "example": {
                "photos": [],
                "total": 0
            }
        }
