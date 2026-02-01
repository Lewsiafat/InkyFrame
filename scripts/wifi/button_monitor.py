import time
import subprocess
import logging
import sys
from pathlib import Path

# Try to import gpiod (new way for Pi 5 / Bookworm)
try:
    import gpiod
    import gpiodevice
    from gpiod.line import Bias, Direction, Edge
    GPIO_AVAILABLE = True
except ImportError:
    GPIO_AVAILABLE = False

# Configuration
BUTTON_PIN = 5  # Button A
LONG_PRESS_TIME = 5 # seconds
DEBOUNCE_TIME = 0.1

# Service Names
SERVICE_MAIN = "inky-main"
SERVICE_WIFI = "inky-wifi"

# Config Path (Same as ConfigManager)
CONFIG_PATH_BOOT = Path("/boot/inky_wifi.json")
CONFIG_PATH_LOCAL = Path("/home/pi/Documents/workspaceEink/myInky/wifi_config.json") # Adjust path if needed

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("inky-monitor")

def is_wifi_configured():
    return CONFIG_PATH_BOOT.exists() or CONFIG_PATH_LOCAL.exists()

def run_command(cmd):
    try:
        subprocess.run(cmd, shell=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed: {cmd} - {e}")
        return False

def get_active_service():
    """Check which service is currently active."""
    # This is a bit naive, checks if active.
    if subprocess.run(f"systemctl is-active --quiet {SERVICE_WIFI}", shell=True).returncode == 0:
        return SERVICE_WIFI
    if subprocess.run(f"systemctl is-active --quiet {SERVICE_MAIN}", shell=True).returncode == 0:
        return SERVICE_MAIN
    return None

def switch_mode():
    """Toggle between modes."""
    active = get_active_service()
    logger.info(f"Switching mode. Active: {active}")
    
    if active == SERVICE_WIFI:
        # Switch to Main
        logger.info("Switching to Main App...")
        run_command(f"sudo systemctl stop {SERVICE_WIFI}")
        run_command(f"sudo systemctl start {SERVICE_MAIN}")
    
    elif active == SERVICE_MAIN:
        # Switch to WiFi
        logger.info("Switching to WiFi Setup...")
        run_command(f"sudo systemctl stop {SERVICE_MAIN}")
        run_command(f"sudo systemctl start {SERVICE_WIFI}")
        
    else:
        # Neither is running? Start Main if config exists, else WiFi
        logger.info("No service active. Starting default based on config.")
        if is_wifi_configured():
            run_command(f"sudo systemctl start {SERVICE_MAIN}")
        else:
            run_command(f"sudo systemctl start {SERVICE_WIFI}")

def monitor_loop():
    logger.info("Starting Button Monitor (gpiod)...")
    
    # Check boot state once
    active = get_active_service()
    if not active:
        logger.info("Initial Boot Check...")
        if is_wifi_configured():
            logger.info("Config found. Ensuring Main App starts.")
            run_command(f"sudo systemctl start {SERVICE_MAIN}")
        else:
            logger.info("No config found. Starting WiFi Setup.")
            run_command(f"sudo systemctl start {SERVICE_WIFI}")

    if not GPIO_AVAILABLE:
        logger.warning("gpiod/gpiodevice not available - Button monitoring disabled")
        while True:
            time.sleep(60)

    try:
        # Setup GPIO using gpiod and gpiodevice
        chip = gpiodevice.find_chip_by_platform()
        
        # Configure the line for Button A
        # We need both edges to detect press (falling) and release (rising)
        # Note: Inky usually has Pull-Up, so Press = Low (Falling edge)
        settings = gpiod.LineSettings(
            direction=Direction.INPUT, 
            bias=Bias.PULL_UP, 
            edge_detection=Edge.BOTH
        )
        
        # Get offset for line
        offset = chip.line_offset_from_id(BUTTON_PIN)
        
        line_config = {offset: settings}
        request = chip.request_lines(consumer="inky-monitor", config=line_config)
        
        logger.info(f"Monitoring Button A (GPIO {BUTTON_PIN})")

        press_start_time = None
        
        while True:
            # Block and wait for events (timeout 1s to allow loop to check other things if needed)
            for event in request.read_edge_events(timeout=1.0):
                if event.line_offset == offset:
                    
                    # Falling Edge = Pressed (because Pull Up)
                    if event.event_type == gpiod.EdgeEvent.Type.FALLING_EDGE:
                        press_start_time = time.time()
                        logger.debug("Button Pressed")
                        
                    # Rising Edge = Released
                    elif event.event_type == gpiod.EdgeEvent.Type.RISING_EDGE:
                        if press_start_time:
                            duration = time.time() - press_start_time
                            logger.debug(f"Button Released. Duration: {duration:.2f}s")
                            # Check for long press on release (or check continuously?)
                            # Checking on release is safer for simple logic, but let's check holding too
                            press_start_time = None
            
            # Continuous check for long press while held
            if press_start_time:
                # We need to manually check if it's still pressed? 
                # gpiod events are good, but if we miss one? 
                # With read_edge_events, we rely on the state tracking.
                
                # Check current value to be sure?
                # request.get_value(offset) might be needed if we want to poll
                
                duration = time.time() - press_start_time
                if duration > LONG_PRESS_TIME:
                    logger.info("Long Press Detected! Triggering Switch.")
                    switch_mode()
                    
                    # Reset
                    press_start_time = None
                    # Wait for release (we will see rising edge later, but ignore it)
                    
            # Heartbeat or other checks
            
    except Exception as e:
        logger.error(f"GPIO Error: {e}")
        # Sleep a bit to avoid busy loop on failure
        time.sleep(5)

if __name__ == "__main__":
    monitor_loop()
