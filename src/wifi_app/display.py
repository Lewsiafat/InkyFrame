import logging
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import qrcode
from src.wifi_app.network_manager import NetworkManager

logger = logging.getLogger(__name__)

class WifiDisplay:
    """Manages display output for the WiFi setup app."""
    
    def __init__(self):
        self._display = None
        self._font = None
        self._font_large = None
        self._init_hw()
        
    def _init_hw(self):
        try:
            from inky.auto import auto
            self._display = auto()
            logger.info(f"Inky display initialized for WiFi App: {self._display.width}x{self._display.height}")
        except ImportError:
            logger.warning("Inky library not found, running in mock mode")
            self._display = None
        except Exception as e:
            logger.error(f"Inky init failed: {e}")
            self._display = None

    def _get_font(self, size=24):
        try:
            # Try to load a standard font
            return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size)
        except:
            return ImageFont.load_default()

    def show_ap_mode(self, ssid: str, password: str, ip: str):
        """Show AP Mode status with QR Code."""
        if not self._display:
            logger.info(f"MOCK DISPLAY: AP Mode | SSID: {ssid} | PASS: {password} | IP: {ip}")
            return

        width, height = self._display.width, self._display.height
        image = Image.new("P", (width, height), self._display.WHITE)
        draw = ImageDraw.Draw(image)
        
        # Fonts
        font_title = self._get_font(40)
        font_text = self._get_font(24)
        
        # 1. Text Info (Left side)
        margin = 30
        y = 40
        
        draw.text((margin, y), "Inky Setup Mode", fill=self._display.BLACK, font=font_title)
        y += 60
        draw.text((margin, y), f"SSID: {ssid}", fill=self._display.BLACK, font=font_text)
        y += 40
        draw.text((margin, y), f"Pass: {password}", fill=self._display.BLACK, font=font_text)
        y += 40
        draw.text((margin, y), f"URL: http://{ip}:8000", fill=self._display.BLACK, font=font_text)
        y += 80
        draw.text((margin, y), "Waiting for configuration...", fill=self._display.RED, font=font_text)
        
        # 2. QR Code (Right side)
        # Format: WIFI:S:MySSID;T:WPA;P:MyPass;;
        qr_data = f"WIFI:S:{ssid};T:WPA;P:{password};;"
        qr = qrcode.QRCode(box_size=10, border=2)
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        qr_img = qr.make_image(fill_color="black", back_color="white")
        qr_size = min(350, height - 60)
        qr_img = qr_img.resize((qr_size, qr_size))
        
        # Center QR on right half
        qr_x = width - qr_size - 40
        qr_y = (height - qr_size) // 2
        
        image.paste(qr_img, (qr_x, qr_y))
        
        self._display.set_image(image)
        self._display.show()

    def show_connecting(self, target_ssid: str):
        """Show connecting status."""
        logger.info(f"Displaying: Connecting to {target_ssid}...")
        self._render_message("Connecting...", f"Target: {target_ssid}")

    def show_success(self, ssid: str, ip: str):
        """Show success status."""
        logger.info(f"Displaying: Connected to {ssid}, IP: {ip}")
        self._render_message("Connected!", f"WiFi: {ssid}", f"IP: {ip}", color=self._display.GREEN if self._display else 0)

    def show_fail(self, ssid: str, error: str):
        """Show failure status."""
        logger.info(f"Displaying: Failed to connect to {ssid}. Error: {error}")
        self._render_message("Connection Failed", f"Network: {ssid}", f"Error: {error}", color=self._display.RED if self._display else 0)

    def _render_message(self, title: str, *lines, color=None):
        if not self._display:
            return
            
        width, height = self._display.width, self._display.height
        image = Image.new("P", (width, height), self._display.WHITE)
        draw = ImageDraw.Draw(image)
        
        font_title = self._get_font(48)
        font_text = self._get_font(32)
        
        color = color or self._display.BLACK
        
        # Center text
        y = height // 3
        
        w = draw.textlength(title, font=font_title)
        draw.text(((width - w) / 2, y), title, fill=color, font=font_title)
        y += 70
        
        for line in lines:
            w = draw.textlength(line, font=font_text)
            draw.text(((width - w) / 2, y), line, fill=self._display.BLACK, font=font_text)
            y += 50
            
        self._display.set_image(image)
        self._display.show()

wifi_display = WifiDisplay()
