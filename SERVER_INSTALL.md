# Server Installation Guide

This guide covers the manual installation steps you need to perform on the development board after deploying the files.

## Prerequisites

- Development board: `lewsiafat@192.168.31.90`
- Project path: `/home/lewsiafat/Documents/workspaceEink/myInky`
- Files already transferred via deployment script

---

## Step 1: SSH into the Server

```bash
ssh lewsiafat@192.168.31.90
```

---

## Step 2: Navigate to Project Directory

```bash
cd /home/lewsiafat/Documents/workspaceEink/myInky
```

---

## Step 3: Install uv (if not already installed)

Check if `uv` is installed:
```bash
which uv
```

If not installed, install it:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Then reload your shell configuration:
```bash
source $HOME/.cargo/env
```

Or for zsh:
```bash
source $HOME/.zshrc
```

Verify installation:
```bash
uv --version
```

---

## Step 4: Install Python Dependencies

```bash
uv sync
```

This will:
- Create a virtual environment in `.venv`
- Install all required packages (FastAPI, Pillow, numpy, etc.)

---

## Step 5: Create Upload Directories

```bash
mkdir -p uploads/originals uploads/optimized uploads/thumbnails
```

---

## Step 6: Start the Server

### Option A: Foreground (for testing)

```bash
uv run uvicorn src.main:app --host 0.0.0.0 --port 8000
```

Press `Ctrl+C` to stop.

### Option B: Background (persistent)

```bash
nohup uv run uvicorn src.main:app --host 0.0.0.0 --port 8000 > server.log 2>&1 &
```

Check if running:
```bash
ps aux | grep uvicorn
```

View logs:
```bash
tail -f server.log
```

Stop server:
```bash
pkill -f "uvicorn src.main:app"
```

---

## Step 7: Access the Application

Open your browser and navigate to:

**http://192.168.31.90:8000**

You should see the Inky Photo Display web interface!

---

## Optional: Set Up Systemd Service (Auto-start on boot)

### 1. Create service file

```bash
sudo nano /etc/systemd/system/inky-server.service
```

### 2. Add this configuration

```ini
[Unit]
Description=Inky Photo Display Web Server
After=network.target

[Service]
Type=simple
User=lewsiafat
WorkingDirectory=/home/lewsiafat/Documents/workspaceEink/myInky
ExecStart=/home/lewsiafat/.local/bin/uv run uvicorn src.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10
StandardOutput=append:/home/lewsiafat/Documents/workspaceEink/myInky/server.log
StandardError=append:/home/lewsiafat/Documents/workspaceEink/myInky/server.log

[Install]
WantedBy=multi-user.target
```

**Note:** Adjust the `ExecStart` path if `uv` is installed in a different location. Check with:
```bash
which uv
```

### 3. Enable and start the service

```bash
sudo systemctl daemon-reload
sudo systemctl enable inky-server
sudo systemctl start inky-server
```

### 4. Check service status

```bash
sudo systemctl status inky-server
```

### 5. View logs

```bash
sudo journalctl -u inky-server -f
```

### 6. Service management commands

```bash
# Stop service
sudo systemctl stop inky-server

# Restart service
sudo systemctl restart inky-server

# Disable auto-start
sudo systemctl disable inky-server
```

---

## Troubleshooting

### uv command not found

If `uv` is not in your PATH after installation:

```bash
# Add to your shell config
echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

Or for zsh:
```bash
echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### Port 8000 already in use

Check what's using the port:
```bash
lsof -i :8000
```

Kill the process:
```bash
kill -9 <PID>
```

Or use a different port:
```bash
uv run uvicorn src.main:app --host 0.0.0.0 --port 8080
```

### Permission denied for GPIO (Inky display)

Add your user to the gpio group:
```bash
sudo usermod -a -G gpio lewsiafat
```

Then log out and log back in.

### Dependencies installation fails

Make sure you have Python 3.11+:
```bash
python3 --version
```

If needed, install Python 3.11:
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv
```

---

## Quick Reference

| Task | Command |
|------|---------|
| Start server (foreground) | `uv run uvicorn src.main:app --host 0.0.0.0 --port 8000` |
| Start server (background) | `nohup uv run uvicorn src.main:app --host 0.0.0.0 --port 8000 > server.log 2>&1 &` |
| Stop server | `pkill -f "uvicorn src.main:app"` |
| Check if running | `ps aux \| grep uvicorn` |
| View logs | `tail -f server.log` |
| Restart systemd service | `sudo systemctl restart inky-server` |
| Check service status | `sudo systemctl status inky-server` |

---

## Environment Variables (Optional)

You can set these before starting the server:

```bash
export HOST=0.0.0.0
export PORT=8000
export INKY_MODEL=auto
```

Or create a `.env` file in the project directory.

---

## Next Steps

1. ✅ Upload a test photo via the web interface
2. ✅ Verify image optimization works
3. ✅ Test displaying on the Inky e-ink display
4. ✅ Set up systemd service for auto-start (optional)

For more details, see [DEPLOYMENT.md](DEPLOYMENT.md).
