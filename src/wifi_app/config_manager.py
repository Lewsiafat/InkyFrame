import json
import os
from pathlib import Path
from typing import Optional, Dict
import logging

logger = logging.getLogger(__name__)

class ConfigManager:
    """Manages reading and writing WiFi configuration."""
    
    # Locations to check for config. Priority:
    # 1. /boot/inky_wifi.json (User placed file on SD card)
    # 2. ./wifi_config.json (Local persistence)
    BOOT_CONFIG_PATH = Path("/boot/inky_wifi.json")
    LOCAL_CONFIG_PATH = Path("wifi_config.json")
    
    @classmethod
    def load_config(cls) -> Optional[Dict[str, str]]:
        """Load WiFi config from file."""
        # Check boot config first (e.g. user manually placed file)
        if cls.BOOT_CONFIG_PATH.exists():
            try:
                config = json.loads(cls.BOOT_CONFIG_PATH.read_text())
                logger.info("Loaded config from /boot")
                # Optional: Copy to local and delete from boot? 
                # For now, just return it.
                return config
            except Exception as e:
                logger.error(f"Failed to read boot config: {e}")
        
        # Check local config
        if cls.LOCAL_CONFIG_PATH.exists():
            try:
                config = json.loads(cls.LOCAL_CONFIG_PATH.read_text())
                logger.info("Loaded local config")
                return config
            except Exception as e:
                logger.error(f"Failed to read local config: {e}")
                
        return None

    @classmethod
    def save_config(cls, ssid: str, password: str):
        """Save WiFi config to local file."""
        config = {"ssid": ssid, "password": password}
        try:
            cls.LOCAL_CONFIG_PATH.write_text(json.dumps(config, indent=2))
            # Ensure lewsiafat can read/write it (since we might be running as root)
            try:
                import shutil
                shutil.chown(cls.LOCAL_CONFIG_PATH, user="lewsiafat", group="lewsiafat")
                cls.LOCAL_CONFIG_PATH.chmod(0o666)
            except Exception as owner_err:
                logger.warning(f"Could not change config ownership: {owner_err}")
                
            logger.info(f"Saved config for {ssid}")
        except Exception as e:
            logger.error(f"Failed to save config: {e}")
            raise

    @classmethod
    def has_config(cls) -> bool:
        """Check if any config exists."""
        return cls.BOOT_CONFIG_PATH.exists() or cls.LOCAL_CONFIG_PATH.exists()
