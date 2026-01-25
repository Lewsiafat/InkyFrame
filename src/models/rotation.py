"""Data models for rotation schedule feature."""
from pydantic import BaseModel, Field
from typing import List, Literal


class RotationItem(BaseModel):
    """Single item in rotation playlist."""
    type: Literal["photo", "weather"]
    photo_id: str | None = None  # Only required for photo type
    
    class Config:
        json_schema_extra = {
            "examples": [
                {"type": "photo", "photo_id": "abc123"},
                {"type": "weather"}
            ]
        }


class RotationPlaylist(BaseModel):
    """Rotation playlist configuration."""
    items: List[RotationItem] = Field(default_factory=list)
    interval_minutes: int = Field(default=30, ge=5, le=1440)
    enabled: bool = False
    
    class Config:
        json_schema_extra = {
            "example": {
                "items": [
                    {"type": "photo", "photo_id": "abc123"},
                    {"type": "weather"},
                    {"type": "photo", "photo_id": "def456"}
                ],
                "interval_minutes": 30,
                "enabled": True
            }
        }


class RotationStatus(BaseModel):
    """Current rotation status."""
    enabled: bool
    current_index: int
    current_item: RotationItem | None = None
    next_update: str | None = None  # ISO timestamp
    playlist_size: int
    interval_minutes: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "enabled": True,
                "current_index": 1,
                "current_item": {"type": "weather"},
                "next_update": "2026-01-25T21:00:00+08:00",
                "playlist_size": 3,
                "interval_minutes": 30
            }
        }
