"""API endpoints for rotation schedule."""
from fastapi import APIRouter, HTTPException
from typing import List

from ..models.rotation import RotationPlaylist, RotationStatus, RotationItem
from ..services.rotation_scheduler import rotation_scheduler

router = APIRouter(prefix="/api/rotation", tags=["rotation"])


@router.post("/start", response_model=RotationStatus)
async def start_rotation(playlist: RotationPlaylist):
    """Start rotation with given playlist.
    
    Args:
        playlist: Rotation playlist configuration
        
    Returns:
        Current rotation status
        
    Raises:
        HTTPException: If playlist is empty or invalid
    """
    if not playlist.items:
        raise HTTPException(status_code=400, detail="Playlist cannot be empty")
    
    try:
        await rotation_scheduler.start_rotation(
            items=playlist.items,
            interval_minutes=playlist.interval_minutes
        )
        return rotation_scheduler.get_status()
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start rotation: {str(e)}")


@router.post("/stop", response_model=RotationStatus)
async def stop_rotation():
    """Stop rotation.
    
    Returns:
        Current rotation status
    """
    try:
        await rotation_scheduler.stop_rotation()
        return rotation_scheduler.get_status()
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to stop rotation: {str(e)}")


@router.get("/status", response_model=RotationStatus)
async def get_rotation_status():
    """Get current rotation status.
    
    Returns:
        Current rotation status including enabled state, current item, and next update time
    """
    return rotation_scheduler.get_status()


@router.post("/next", response_model=RotationStatus)
async def skip_to_next():
    """Skip to next item immediately.
    
    Returns:
        Current rotation status
        
    Raises:
        HTTPException: If rotation is not active
    """
    try:
        await rotation_scheduler.skip_to_next()
        return rotation_scheduler.get_status()
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to skip: {str(e)}")
