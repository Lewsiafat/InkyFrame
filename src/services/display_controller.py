"""Display controller service for managing Inky e-ink display."""
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Optional
import logging

from src.models.photo import DisplayStatus

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DisplayController:
    """Service for controlling the Inky e-ink display."""
    
    def __init__(self):
        """Initialize display controller."""
        self.status = DisplayStatus.IDLE
        self.current_photo_id: Optional[str] = None
        self.last_update: Optional[datetime] = None
        self._updating_lock = asyncio.Lock()
        self._display = None
    
    def _init_display(self):
        """Initialize the Inky display hardware."""
        if self._display is not None:
            return
        
        try:
            # Try to import and auto-detect Inky display
            from inky.auto import auto
            self._display = auto()
            logger.info(f"Inky display initialized: {self._display.width}x{self._display.height}")
        except ImportError:
            logger.warning("Inky library not available - running in mock mode")
            self._display = None
        except Exception as e:
            logger.error(f"Failed to initialize Inky display: {e}")
            self._display = None
    
    async def display_photo(self, image_path: Path, photo_id: str) -> bool:
        """
        Display a photo on the Inky e-ink display.
        
        Args:
            image_path: Path to optimized image file
            photo_id: Photo UUID
            
        Returns:
            True if successful, False otherwise
        """
        # Prevent concurrent updates
        if self._updating_lock.locked():
            logger.warning("Display update already in progress")
            return False
        
        async with self._updating_lock:
            try:
                self.status = DisplayStatus.UPDATING
                logger.info(f"Starting display update for photo {photo_id}")
                
                # Initialize display if needed
                self._init_display()
                
                if self._display is None:
                    # Mock mode - simulate display update
                    logger.info(f"Mock mode: Would display {image_path}")
                    await asyncio.sleep(2)  # Simulate display time
                else:
                    # Real display mode
                    from PIL import Image
                    
                    # Load optimized image
                    image = Image.open(image_path)
                    
                    # Set image on display
                    self._display.set_image(image)
                    
                    # Update display (this blocks for ~20-25 seconds)
                    await asyncio.to_thread(self._display.show)
                
                # Update status
                self.status = DisplayStatus.IDLE
                self.current_photo_id = photo_id
                self.last_update = datetime.now()
                
                logger.info(f"Display update completed for photo {photo_id}")
                return True
                
            except Exception as e:
                logger.error(f"Display update failed: {e}")
                self.status = DisplayStatus.ERROR
                return False
    
    def get_status(self) -> dict:
        """
        Get current display status.
        
        Returns:
            Dictionary with status information
        """
        return {
            "status": self.status,
            "current_photo_id": self.current_photo_id,
            "last_update": self.last_update
        }


# Global display controller instance
display_controller = DisplayController()
