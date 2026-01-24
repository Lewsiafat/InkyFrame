"""Photo upload API endpoints."""
from fastapi import APIRouter, UploadFile, File, HTTPException, status
from datetime import datetime

from src.models.photo import PhotoMetadata
from src.services.storage import StorageService
from src.services.image_processor import ImageProcessor
from src.config import MAX_FILE_SIZE, ALLOWED_EXTENSIONS

router = APIRouter(prefix="/api", tags=["upload"])


@router.post("/upload", response_model=PhotoMetadata, status_code=status.HTTP_201_CREATED)
async def upload_photo(file: UploadFile = File(...)):
    """
    Upload a photo.
    
    Args:
        file: Uploaded image file
        
    Returns:
        Photo metadata
        
    Raises:
        HTTPException: If file validation fails
    """
    # Validate file extension
    file_ext = file.filename.split('.')[-1].lower() if '.' in file.filename else ''
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # Read file content
    content = await file.read()
    
    # Validate file size
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File too large. Maximum size: {MAX_FILE_SIZE / 1024 / 1024:.1f}MB"
        )
    
    # Validate that it's actually an image
    try:
        from PIL import Image
        import io
        Image.open(io.BytesIO(content)).verify()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid image file"
        )
    
    # Save original file
    photo_id, original_path = await StorageService.save_upload(content, file.filename)
    
    # Process image (create optimized version and thumbnail)
    try:
        await ImageProcessor.process_upload(original_path, photo_id)
    except Exception as e:
        # Clean up if processing fails
        await StorageService.delete_photo(photo_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Image processing failed: {str(e)}"
        )
    
    # Return metadata
    return PhotoMetadata(
        id=photo_id,
        filename=file.filename,
        size=len(content),
        timestamp=datetime.now(),
        thumbnail_url=f"/api/photos/{photo_id}/thumbnail"
    )
