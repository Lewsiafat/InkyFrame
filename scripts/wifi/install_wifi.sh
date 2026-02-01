#!/bin/bash
set -e

echo "Installing Inky WiFi App Services..."

# 1. Install dependencies
# Install system dependencies
# - dnsmasq: for Hotspot DHCP
# - swig, python3-dev, gcc: for building rpi-lgpio
echo "Installing system dependencies..."
sudo apt-get update
sudo apt-get install -y dnsmasq swig python3-dev gcc liblgpio-dev

# Disable system-wide dnsmasq so NetworkManager can manage it for Hotspot
echo "Disabling system-wide dnsmasq to avoid conflicts..."
sudo systemctl stop dnsmasq || true
sudo systemctl disable dnsmasq || true

echo "Installing Python dependencies..."
/home/lewsiafat/.local/bin/uv pip install qrcode[pil] jinja2 python-multipart inky rpi-lgpio gpiod gpiodevice

# 2. Copy Service Files
echo "Copying service files..."
sudo cp scripts/services/inky-wifi.service /etc/systemd/system/
sudo cp scripts/services/inky-monitor.service /etc/systemd/system/

# 3. Reload Systemd
echo "Reloading systemd..."
sudo systemctl daemon-reload

# 4. Enable Monitor (always runs)
echo "Enabling Monitor Service..."
sudo systemctl enable inky-monitor.service
sudo systemctl start inky-monitor.service

# 5. Disable WiFi App (managed by monitor)
sudo systemctl disable inky-wifi.service

echo "Installation Complete!"
echo "Monitor is running. It will determine whether to start Main or WiFi app."
