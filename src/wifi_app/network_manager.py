import subprocess
import logging
from typing import List, Optional, Dict

logger = logging.getLogger(__name__)

class NetworkManager:
    """Wrapper for nmcli to manage WiFi connections on Debian 13/Bookworm."""
    
    HOTSPOT_CON_NAME = "Hotspot"
    INITIAL_SSID = "InkySetup"
    INITIAL_PASS = "inky1234" # Default password for AP, though open is also an option if desired

    @staticmethod
    def run_command(cmd: List[str]) -> str:
        """Run nmcli command and return output."""
        try:
            logger.info(f"Running command: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            logger.error(f"Command failed: {e.stderr}")
            raise Exception(f"nmcli command failed: {e.stderr}")

    @classmethod
    def create_hotspot(cls, ssid: str = INITIAL_SSID, password: str = INITIAL_PASS):
        """Create and activate a WiFi Hotspot (AP mode)."""
        logger.info(f"Creating Hotspot with SSID: {ssid}")
        
        # 1. Clean up existing connections to avoid conflict
        cls.disconnect_all()
        
        # 2. Add connection
        # Debian 13 nmcli syntax for AP mode
        # '802-11-wireless.mode ap' and 'ipv4.method shared' are key
        cmd = [
            "nmcli", "con", "add", "type", "wifi",
            "ifname", "wlan0",
            "con-name", cls.HOTSPOT_CON_NAME,
            "autoconnect", "yes",
            "ssid", ssid,
            "802-11-wireless.mode", "ap",
            "ipv4.method", "shared"
        ]
        
        if password:
            cmd.extend(["wifi-sec.key-mgmt", "wpa-psk"])
            cmd.extend(["wifi-sec.psk", password])
            
        try:
            cls.run_command(cmd)
            # 3. Activate
            cls.run_command(["nmcli", "con", "up", cls.HOTSPOT_CON_NAME])
            logger.info("Hotspot created and activated successfully.")
        except Exception as e:
            logger.error(f"Failed to create hotspot: {e}")
            raise

    @classmethod
    def connect_to_wifi(cls, ssid: str, password: str):
        """Connect to a WiFi network (Client mode)."""
        logger.info(f"Connecting to WiFi: {ssid}")
        
        # 1. Remove Hotspot if active
        try:
            cls.run_command(["nmcli", "con", "delete", cls.HOTSPOT_CON_NAME])
        except:
            pass # Ignore if not exists at all
            
        # 2. Connect
        cmd = ["nmcli", "dev", "wifi", "connect", ssid]
        if password:
            cmd.extend(["password", password])
            
        try:
            cls.run_command(cmd)
            logger.info(f"Successfully connected to {ssid}")
        except Exception as e:
            logger.error(f"Failed to connect to {ssid}: {e}")
            raise

    @classmethod
    def disconnect_all(cls):
        """Disconnect all active WiFi connections."""
        try:
            # Get active connection on wlan0
            # This is a bit rough, might need refinement to only target wifi
            cls.run_command(["nmcli", "device", "disconnect", "wlan0"])
        except Exception as e:
            logger.warning(f"Disconnect warning (might be already disconnected): {e}")

    @classmethod
    def scan_networks(cls) -> List[str]:
        """Scan for available WiFi networks."""
        try:
            # -f SSID means only output SSID field
            output = cls.run_command(["nmcli", "-f", "SSID", "dev", "wifi", "list", "--rescan", "yes"])
            ssids = [line.strip() for line in output.split('\n') if line.strip() and line.strip() != "SSID"]
            # Remove duplicates and empty strings
            unique_ssids = sorted(list(set(filter(None, ssids))))
            return unique_ssids
        except Exception as e:
            logger.error(f"Scan failed: {e}")
            return []

    @classmethod
    def get_ip_address(cls) -> str:
        """Get current IP address of wlan0."""
        try:
            output = cls.run_command(["nmcli", "-g", "ip4.address", "dev", "show", "wlan0"])
            # Output might be '192.168.1.100/24'
            return output.split('/')[0] if output else "Unknown"
        except Exception:
            return "Unknown"
