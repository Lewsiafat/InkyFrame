"""State persistence for rotation schedule."""
import json
from pathlib import Path
from typing import List, Dict, Any
import logging

from ..config import BASE_DIR

logger = logging.getLogger(__name__)

ROTATION_STATE_FILE = BASE_DIR / "rotation_state.json"


class RotationState:
    """Manage rotation state persistence."""
    
    @staticmethod
    def save_state(playlist: List[Dict[str, Any]], enabled: bool, current_index: int, interval_minutes: int) -> None:
        """Save rotation state to JSON file.
        
        Args:
            playlist: List of rotation items
            enabled: Whether rotation is enabled
            current_index: Current position in playlist
            interval_minutes: Rotation interval in minutes
        """
        try:
            state = {
                "playlist": playlist,
                "enabled": enabled,
                "current_index": current_index,
                "interval_minutes": interval_minutes
            }
            
            with open(ROTATION_STATE_FILE, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=2)
                
            logger.info(f"Rotation state saved: {len(playlist)} items, enabled={enabled}")
            
        except Exception as e:
            logger.error(f"Failed to save rotation state: {e}")
    
    @staticmethod
    def load_state() -> Dict[str, Any] | None:
        """Load rotation state from JSON file.
        
        Returns:
            State dictionary or None if file doesn't exist or is invalid
        """
        try:
            if not ROTATION_STATE_FILE.exists():
                logger.info("No rotation state file found")
                return None
            
            with open(ROTATION_STATE_FILE, 'r', encoding='utf-8') as f:
                state = json.load(f)
            
            logger.info(f"Rotation state loaded: {len(state.get('playlist', []))} items")
            return state
            
        except Exception as e:
            logger.error(f"Failed to load rotation state: {e}")
            return None
    
    @staticmethod
    def clear_state() -> None:
        """Clear rotation state file."""
        try:
            if ROTATION_STATE_FILE.exists():
                ROTATION_STATE_FILE.unlink()
                logger.info("Rotation state cleared")
        except Exception as e:
            logger.error(f"Failed to clear rotation state: {e}")
