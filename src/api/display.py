"""Display control API endpoints."""
from fastapi import APIRouter, HTTPException, status, BackgroundTasks

from src.models.photo import DisplayRequest, DisplayResponse, StatusResponse, DisplayStatus
from src.services.storage import StorageService
from src.services.display_controller import display_controller

router = APIRouter(prefix="/api", tags=["display"])


@router.post("/display/{photo_id}", response_model=DisplayResponse, status_code=status.HTTP_202_ACCEPTED)
async def display_photo(
    photo_id: str,
    request: DisplayRequest = DisplayRequest(),
    background_tasks: BackgroundTasks = None
):
    """
    Display a photo on the Inky e-ink display.
    
    Args:
        photo_id: Photo UUID
        request: Display request parameters
        background_tasks: FastAPI background tasks
        
    Returns:
        Display response with status
        
    Raises:
        HTTPException: If photo not found or display busy
    """
    # Check if photo exists
    optimized_path = StorageService.get_optimized_path(photo_id)
    if not optimized_path:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Photo not found or not yet optimized"
        )
    
    # Check if display is already updating
    if display_controller.status == DisplayStatus.UPDATING:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Display update already in progress"
        )
    
    # Start display update in background
    background_tasks.add_task(
        display_controller.display_photo,
        optimized_path,
        photo_id
    )
    
    return DisplayResponse(
        status=DisplayStatus.UPDATING,
        estimated_time=25,
        message="Display update started"
    )


@router.get("/status", response_model=StatusResponse)
async def get_status():
    """
    Get current display status.
    
    Returns:
        Display status information
    """
    status_info = display_controller.get_status()
    return StatusResponse(**status_info)
