"""Photo gallery API endpoints."""
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse
from datetime import datetime

from src.models.photo import PhotoMetadata, PhotoDetail, PhotoListResponse
from src.services.storage import StorageService

router = APIRouter(prefix="/api/photos", tags=["gallery"])


@router.get("", response_model=PhotoListResponse)
async def list_photos():
    """
    List all uploaded photos.
    
    Returns:
        List of photo metadata
    """
    photos = []
    for photo_id, file_path in StorageService.list_all_photos():
        # Get file stats
        stat = file_path.stat()
        
        photos.append(PhotoMetadata(
            id=photo_id,
            filename=file_path.name,
            size=stat.st_size,
            timestamp=datetime.fromtimestamp(stat.st_mtime),
            thumbnail_url=f"/api/photos/{photo_id}/thumbnail"
        ))
    
    # Sort by timestamp (newest first)
    photos.sort(key=lambda p: p.timestamp, reverse=True)
    
    return PhotoListResponse(photos=photos, total=len(photos))


@router.get("/{photo_id}", response_model=PhotoDetail)
async def get_photo(photo_id: str):
    """
    Get detailed information about a specific photo.
    
    Args:
        photo_id: Photo UUID
        
    Returns:
        Detailed photo information
        
    Raises:
        HTTPException: If photo not found
    """
    original_path = StorageService.get_original_path(photo_id)
    if not original_path:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Photo not found"
        )
    
    stat = original_path.stat()
    optimized_path = StorageService.get_optimized_path(photo_id)
    
    return PhotoDetail(
        id=photo_id,
        filename=original_path.name,
        size=stat.st_size,
        timestamp=datetime.fromtimestamp(stat.st_mtime),
        thumbnail_url=f"/api/photos/{photo_id}/thumbnail",
        original_url=f"/uploads/originals/{original_path.name}",
        optimized_url=f"/uploads/optimized/{photo_id}.jpg" if optimized_path else None
    )


@router.get("/{photo_id}/thumbnail")
async def get_thumbnail(photo_id: str):
    """
    Get photo thumbnail.
    
    Args:
        photo_id: Photo UUID
        
    Returns:
        Thumbnail image file
        
    Raises:
        HTTPException: If thumbnail not found
    """
    thumbnail_path = StorageService.get_thumbnail_path(photo_id)
    if not thumbnail_path:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Thumbnail not found"
        )
    
    return FileResponse(thumbnail_path, media_type="image/jpeg")


@router.delete("/{photo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_photo(photo_id: str):
    """
    Delete a photo and all associated files.
    
    Args:
        photo_id: Photo UUID
        
    Raises:
        HTTPException: If photo not found
    """
    deleted = await StorageService.delete_photo(photo_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Photo not found"
        )
