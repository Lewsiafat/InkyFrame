import time
import subprocess
import logging
import sys
from pathlib import Path

# Try to import RPi.GPIO, else mock
try:
    import RPi.GPIO as GPIO
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

def setup_gpio():
    if not GPIO_AVAILABLE:
        logger.warning("GPIO not available - Button monitoring disabled (or Mocked)")
        return
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def monitor_loop():
    logger.info("Starting Button Monitor...")
    setup_gpio()
    
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
        # Just sleep forever if no GPIO (or run logic for testing)
        while True:
            time.sleep(60)

    # Button Loop
    last_state = GPIO.input(BUTTON_PIN)
    press_start_time = None
    
    while True:
        current_state = GPIO.input(BUTTON_PIN)
        
        # Button Pressed (Low)
        if current_state == GPIO.LOW and last_state == GPIO.HIGH:
            press_start_time = time.time()
            logger.debug("Button Press Started")

        # Button Released (High)
        elif current_state == GPIO.HIGH and last_state == GPIO.LOW:
            if press_start_time:
                duration = time.time() - press_start_time
                logger.debug(f"Button Released. Duration: {duration:.2f}s")
                press_start_time = None
        
        # Checking duration while held
        if current_state == GPIO.LOW and press_start_time:
            duration = time.time() - press_start_time
            if duration > LONG_PRESS_TIME:
                logger.info("Long Press Detected! Triggering Switch.")
                switch_mode()
                
                # Wait for release to avoid double trigger
                while GPIO.input(BUTTON_PIN) == GPIO.LOW:
                    time.sleep(0.1)
                press_start_time = None
        
        last_state = current_state
        time.sleep(DEBOUNCE_TIME)

if __name__ == "__main__":
    monitor_loop()
