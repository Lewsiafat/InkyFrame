"""Storage service for managing uploaded files."""
import uuid
from pathlib import Path
from typing import Optional
import aiofiles
import aiofiles.os

from src.config import ORIGINALS_DIR, OPTIMIZED_DIR, THUMBNAILS_DIR


class StorageService:
    """Service for managing file storage."""
    
    @staticmethod
    def generate_unique_filename(original_filename: str) -> tuple[str, str]:
        """
        Generate a unique filename while preserving the extension.
        
        Args:
            original_filename: Original filename with extension
            
        Returns:
            Tuple of (unique_id, extension)
        """
        unique_id = str(uuid.uuid4())
        extension = Path(original_filename).suffix.lower()
        return unique_id, extension
    
    @staticmethod
    async def save_upload(file_content: bytes, filename: str) -> tuple[str, Path]:
        """
        Save uploaded file to originals directory.
        
        Args:
            file_content: File content as bytes
            filename: Original filename
            
        Returns:
            Tuple of (unique_id, saved_path)
        """
        unique_id, extension = StorageService.generate_unique_filename(filename)
        file_path = ORIGINALS_DIR / f"{unique_id}{extension}"
        
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(file_content)
        
        return unique_id, file_path
    
    @staticmethod
    def get_original_path(photo_id: str) -> Optional[Path]:
        """
        Get path to original photo.
        
        Args:
            photo_id: Photo UUID
            
        Returns:
            Path to original file or None if not found
        """
        for ext in ['.jpg', '.jpeg', '.png', '.bmp', '.webp']:
            path = ORIGINALS_DIR / f"{photo_id}{ext}"
            if path.exists():
                return path
        return None
    
    @staticmethod
    def get_optimized_path(photo_id: str) -> Optional[Path]:
        """
        Get path to optimized photo.
        
        Args:
            photo_id: Photo UUID
            
        Returns:
            Path to optimized file or None if not found
        """
        path = OPTIMIZED_DIR / f"{photo_id}.jpg"
        return path if path.exists() else None
    
    @staticmethod
    def get_thumbnail_path(photo_id: str) -> Optional[Path]:
        """
        Get path to thumbnail.
        
        Args:
            photo_id: Photo UUID
            
        Returns:
            Path to thumbnail file or None if not found
        """
        path = THUMBNAILS_DIR / f"{photo_id}.jpg"
        return path if path.exists() else None
    
    @staticmethod
    async def delete_photo(photo_id: str) -> bool:
        """
        Delete all files associated with a photo.
        
        Args:
            photo_id: Photo UUID
            
        Returns:
            True if any files were deleted
        """
        deleted = False
        
        # Delete original
        original_path = StorageService.get_original_path(photo_id)
        if original_path and original_path.exists():
            await aiofiles.os.remove(original_path)
            deleted = True
        
        # Delete optimized
        optimized_path = StorageService.get_optimized_path(photo_id)
        if optimized_path and optimized_path.exists():
            await aiofiles.os.remove(optimized_path)
            deleted = True
        
        # Delete thumbnail
        thumbnail_path = StorageService.get_thumbnail_path(photo_id)
        if thumbnail_path and thumbnail_path.exists():
            await aiofiles.os.remove(thumbnail_path)
            deleted = True
        
        return deleted
    
    @staticmethod
    def list_all_photos() -> list[tuple[str, Path]]:
        """
        List all photos in the originals directory.
        
        Returns:
            List of tuples (photo_id, file_path)
        """
        photos = []
        for file_path in ORIGINALS_DIR.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in {'.jpg', '.jpeg', '.png', '.bmp', '.webp'}:
                photo_id = file_path.stem
                photos.append((photo_id, file_path))
        return photos
