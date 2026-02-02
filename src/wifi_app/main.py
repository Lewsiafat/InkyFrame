import asyncio
import logging
from pathlib import Path
from enum import Enum
from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from src.wifi_app.config_manager import ConfigManager
from src.wifi_app.network_manager import NetworkManager
from src.wifi_app.display import wifi_display

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("wifi_app")

# App & Template Setup
app = FastAPI()
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Determine relative path to static from execution context or hardcode for now
# We'll just put simple CSS in template for simplicity or mount if needed.
# app.mount("/static", StaticFiles(directory="static"), name="static")

class AppState(Enum):
    BOOT = "BOOT"
    AP_MODE = "AP_MODE"
    CONNECTING = "CONNECTING"
    SUCCESS = "SUCCESS"
    FAIL = "FAIL"

class StateMachine:
    def __init__(self):
        self.state = AppState.BOOT
        self.last_error = ""

    async def run(self):
        """Main lifecycle loop."""
        logger.info("WiFi App State Machine Started")
        
        # Check for config
        config = ConfigManager.load_config()
        if config:
            logger.info("Config found, attempting connection...")
            await self.transition_to(AppState.CONNECTING, ssid=config['ssid'], password=config['password'])
        else:
            logger.info("No config found, entering AP Mode.")
            await self.transition_to(AppState.AP_MODE)

    async def transition_to(self, new_state: AppState, **kwargs):
        logger.info(f"Transitioning: {self.state} -> {new_state}")
        self.state = new_state
        
        if new_state == AppState.AP_MODE:
            # Create Hotspot
            try:
                NetworkManager.create_hotspot()
                # Get IP (usually 10.42.0.1 or similar for Shared)
                await asyncio.sleep(5) # Wait for AP to settle
                ip = NetworkManager.get_ip_address()
                wifi_display.show_ap_mode(
                    ssid=NetworkManager.INITIAL_SSID,
                    password=NetworkManager.INITIAL_PASS,
                    ip=ip
                )
            except Exception as e:
                logger.error(f"Failed to enter AP Mode: {e}")
        
        elif new_state == AppState.CONNECTING:
            ssid = kwargs.get('ssid')
            password = kwargs.get('password')
            try:
                wifi_display.show_connecting(ssid)
            except Exception as e:
                logger.error(f"Display update failed: {e}")
            
            try:
                # Try to connect
                NetworkManager.connect_to_wifi(ssid, password)
                # If no exception, we are connected. Check IP.
                # get_ip_address now has internal retries
                ip = NetworkManager.get_ip_address()
                if ip and ip != "Unknown":
                    await self.transition_to(AppState.SUCCESS, ssid=ssid, ip=ip)
                else:
                    raise Exception("Connected but no IP obtained")
            except Exception as e:
                self.last_error = str(e)
                await self.transition_to(AppState.FAIL, ssid=ssid, error=str(e))

        elif new_state == AppState.SUCCESS:
            ssid = kwargs.get('ssid')
            ip = kwargs.get('ip')
            try:
                wifi_display.show_success(ssid, ip)
            except Exception as e:
                logger.error(f"Display update failed: {e}")
            
            # Save config now that it works
            # (If it came from file, it's already saved, but good to be sure)
            
            # Wait a moment then exit to let supervisor start Main App
            logger.info("Connection successful. Exiting in 15 seconds...")
            await asyncio.sleep(15)
            # Exit with specific code to tell supervisor "Switch to Main"
            import sys
            sys.exit(0) 

        elif new_state == AppState.FAIL:
            ssid = kwargs.get('ssid')
            error = kwargs.get('error')
            try:
                wifi_display.show_fail(ssid, error)
            except Exception as e:
                logger.error(f"Display update failed: {e}")
            
            await asyncio.sleep(5)
            # Revert to AP Mode
            await self.transition_to(AppState.AP_MODE)

fsm = StateMachine()

@app.on_event("startup")
async def startup_event():
    # Start FSM in background
    asyncio.create_task(fsm.run())

# --- Routes ---

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """UI for entering WiFi details."""
    ssids = NetworkManager.scan_networks()
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "ssids": ssids,
        "state": fsm.state.value,
        "error": fsm.last_error
    })

@app.post("/connect")
async def connect(request: Request):
    """Handle form submission."""
    form = await request.form()
    ssid = form.get("ssid")
    password = form.get("password")
    
    if ssid:
        ConfigManager.save_config(ssid, password)
        # Trigger FSM
        asyncio.create_task(fsm.transition_to(AppState.CONNECTING, ssid=ssid, password=password))
        return RedirectResponse(url="/status", status_code=303)
    return RedirectResponse(url="/", status_code=303)

@app.get("/status", response_class=HTMLResponse)
async def status_page(request: Request):
    """Show current connection status."""
    return templates.TemplateResponse("status.html", {
        "request": request,
        "state": fsm.state.value
    })
