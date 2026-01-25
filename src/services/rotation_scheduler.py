"""Rotation scheduler service for automatic display rotation."""
import logging
from datetime import datetime, timedelta
from typing import List
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from ..models.rotation import RotationItem, RotationStatus
from .rotation_state import RotationState
from .display_controller import display_controller
from .storage import storage_service
from .weather_renderer import WeatherRenderer

logger = logging.getLogger(__name__)


class RotationScheduler:
    """Manage automatic rotation between photos and weather."""
    
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.current_index = 0
        self.playlist: List[RotationItem] = []
        self.interval_minutes = 30
        self.enabled = False
        self.next_update_time: datetime | None = None
        
        # Start scheduler (but don't add any jobs yet)
        self.scheduler.start()
        logger.info("Rotation scheduler initialized")
    
    async def start_rotation(self, items: List[RotationItem], interval_minutes: int) -> None:
        """Start rotation with given playlist and interval.
        
        Args:
            items: List of rotation items (photos and/or weather)
            interval_minutes: Rotation interval in minutes
        """
        if not items:
            raise ValueError("Playlist cannot be empty")
        
        # Stop existing rotation if any
        await self.stop_rotation()
        
        # Set new playlist
        self.playlist = items
        self.interval_minutes = interval_minutes
        self.current_index = 0
        self.enabled = True
        
        # Display first item immediately
        await self._rotate_display()
        
        # Schedule periodic rotation
        self.scheduler.add_job(
            self._rotate_display,
            trigger=IntervalTrigger(minutes=interval_minutes),
            id='rotation_job',
            replace_existing=True
        )
        
        # Calculate next update time
        self.next_update_time = datetime.now() + timedelta(minutes=interval_minutes)
        
        # Save state
        self._save_current_state()
        
        logger.info(f"Rotation started: {len(items)} items, interval={interval_minutes}min")
    
    async def stop_rotation(self) -> None:
        """Stop rotation."""
        if self.scheduler.get_job('rotation_job'):
            self.scheduler.remove_job('rotation_job')
        
        self.enabled = False
        self.next_update_time = None
        
        # Save state
        self._save_current_state()
        
        logger.info("Rotation stopped")
    
    async def skip_to_next(self) -> None:
        """Skip to next item immediately."""
        if not self.enabled or not self.playlist:
            raise ValueError("Rotation is not active")
        
        await self._rotate_display()
        
        # Reschedule next rotation
        if self.scheduler.get_job('rotation_job'):
            self.scheduler.reschedule_job(
                'rotation_job',
                trigger=IntervalTrigger(minutes=self.interval_minutes)
            )
            self.next_update_time = datetime.now() + timedelta(minutes=self.interval_minutes)
        
        logger.info("Skipped to next item")
    
    async def _rotate_display(self) -> None:
        """Execute rotation - display next item."""
        if not self.playlist:
            logger.warning("Rotation triggered but playlist is empty")
            return
        
        # Get current item
        item = self.playlist[self.current_index]
        
        try:
            # Display based on type
            if item.type == "photo":
                if not item.photo_id:
                    logger.error("Photo item missing photo_id")
                    return
                
                # Get optimized photo path
                optimized_path = storage_service.get_optimized_path(item.photo_id)
                
                if not optimized_path.exists():
                    logger.error(f"Photo not found: {item.photo_id}")
                    # Skip to next item
                    self.current_index = (self.current_index + 1) % len(self.playlist)
                    self._save_current_state()
                    return
                
                # Display photo
                await display_controller.display_image(optimized_path)
                logger.info(f"Displayed photo: {item.photo_id}")
                
            elif item.type == "weather":
                # Render and display weather
                renderer = WeatherRenderer()
                weather_image = await renderer.render_weather()
                await display_controller.display_pil_image(weather_image)
                logger.info("Displayed weather")
            
            # Move to next index
            self.current_index = (self.current_index + 1) % len(self.playlist)
            
            # Update next update time
            self.next_update_time = datetime.now() + timedelta(minutes=self.interval_minutes)
            
            # Save state
            self._save_current_state()
            
        except Exception as e:
            logger.error(f"Error during rotation: {e}")
    
    def get_status(self) -> RotationStatus:
        """Get current rotation status.
        
        Returns:
            RotationStatus object with current state
        """
        current_item = None
        if self.playlist and 0 <= self.current_index < len(self.playlist):
            # Get the PREVIOUS item (what's currently displayed)
            display_index = (self.current_index - 1) % len(self.playlist)
            current_item = self.playlist[display_index]
        
        return RotationStatus(
            enabled=self.enabled,
            current_index=self.current_index,
            current_item=current_item,
            next_update=self.next_update_time.isoformat() if self.next_update_time else None,
            playlist_size=len(self.playlist),
            interval_minutes=self.interval_minutes
        )
    
    def _save_current_state(self) -> None:
        """Save current state to disk."""
        playlist_data = [item.model_dump() for item in self.playlist]
        RotationState.save_state(
            playlist=playlist_data,
            enabled=self.enabled,
            current_index=self.current_index,
            interval_minutes=self.interval_minutes
        )
    
    async def restore_state(self) -> None:
        """Restore rotation state from disk (on server startup)."""
        state = RotationState.load_state()
        
        if not state or not state.get('enabled'):
            logger.info("No active rotation state to restore")
            return
        
        try:
            # Restore playlist
            items = [RotationItem(**item) for item in state.get('playlist', [])]
            interval = state.get('interval_minutes', 30)
            
            if items:
                await self.start_rotation(items, interval)
                # Restore index
                self.current_index = state.get('current_index', 0)
                logger.info(f"Rotation state restored: {len(items)} items")
        
        except Exception as e:
            logger.error(f"Failed to restore rotation state: {e}")


# Global scheduler instance
rotation_scheduler = RotationScheduler()
