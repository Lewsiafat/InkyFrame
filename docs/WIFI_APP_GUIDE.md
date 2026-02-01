# WiFi Configuration App & Supervisor Guide

This document explains how the new Independent WiFi Setup App works and how to interact with it.

## 🚀 How it Works (The "Supervisor")

We have introduced a **Supervisor Service** (`inky-monitor`) that runs automatically when the Raspberry Pi turns on. It acts as a traffic cop:

1.  **On Boot**: It checks if a WiFi configuration file exists (`wifi_config.json`).
    *   **Config Found?** -> It starts the **Main Photo App**.
    *   **No Config?** -> It starts the **WiFi Setup App**.
2.  **Runtime**: It constantly listens for a **Long Press (5s)** on **Button A**.
    *   If you hold Button A, it **stops the current app and switches to the other one**.

## 🛠 Usage Instructions

### 1. First Run (No WiFi Configured)
After you run the install script, your device likely has no `wifi_config.json` yet.
1.  **Reboot** the Pi (or just wait, the monitor starts automatically).
2.  The **WiFi Setup App** will start.
3.  **On the Display**: You should see a QR Code and "Inky Setup Mode".
4.  **Connect**:
    *   Connect your phone/laptop to the WiFi hotspot: **`InkySetup`** (Password: `inky1234`).
    *   Scan the QR code or go to **`http://10.42.0.1:8000`** (IP may vary, check display).
5.  **Configure**:
    *   Select your home WiFi network.
    *   Enter the password and click Connect.
6.  **Success**: The device will verify the connection, save the config, and **automatically switch to the Main Photo App**.

### 2. Normal Operation
Once configured, the device will always boot straight into the **Main Photo App**.

### 3. Resetting / Changing WiFi
If you move to a new location or need to change WiFi:
1.  Ensure the device is running (displaying photos).
2.  **Press and Hold Button A** (Top Left) for **5 seconds**.
3.  The device will stop the Photo App and switch back to **Setup Mode**.
4.  Follow the "First Run" steps to re-configure.

## 🔍 Troubleshooting

### Check Status
SSH into the Pi to check what is running:

```bash
# Check the Monitor (Should always be "active (running)")
sudo systemctl status inky-monitor

# Check if WiFi App is running
sudo systemctl status inky-wifi

# Check if Main App is running
sudo systemctl status inky-main
```

### View Logs
If something isn't working, check the logs:

```bash
# Monitor Logs (Button presses, switching logic)
journalctl -u inky-monitor -f

# WiFi App Logs (Connection errors)
journalctl -u inky-wifi -f
```

### Manual Override
You can manually force a swap via SSH if needed:
```bash
# Force start Setup Mode
sudo systemctl stop inky-main
sudo systemctl start inky-wifi

# Force start Main App
sudo systemctl stop inky-wifi
sudo systemctl start inky-main
```
