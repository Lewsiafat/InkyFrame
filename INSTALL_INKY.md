# Installing Inky Display Library on Server

This guide shows how to install the Inky e-ink display library on your development board.

## Option 1: Copy Local Inky Library (Recommended)

Since you have the Inky library source in `ref_source/inky`, you can copy it to the server and install it locally.

### Step 1: Copy Inky Library to Server

From your local machine:

```bash
# Copy the inky library folder to the server
scp -r ref_source/inky lewsiafat@192.168.31.90:/home/lewsiafat/Documents/workspaceEink/
```

### Step 2: Install on Server

SSH into the server and install:

```bash
ssh lewsiafat@192.168.31.90
cd /home/lewsiafat/Documents/workspaceEink/inky

# Install the library with uv
uv pip install -e .
```

This installs the Inky library in editable mode from the local source.

---

## Option 2: Install from PyPI

Alternatively, install the published version from PyPI:

```bash
ssh lewsiafat@192.168.31.90
cd /home/lewsiafat/Documents/workspaceEink/myInky

# Add inky to your project dependencies
uv add inky
```

---

## Option 3: Add as Project Dependency

Update your `pyproject.toml` to include the local Inky library:

### On your local machine:

Edit `pyproject.toml` and add:

```toml
[project.dependencies]
# ... existing dependencies ...
inky = {path = "../inky", develop = true}
```

Then redeploy and run `uv sync` on the server.

---

## Verify Installation

After installation, verify it works:

```bash
python3 -c "from inky.auto import auto; print('Inky library installed successfully!')"
```

If you have an Inky display connected, it should auto-detect:

```bash
python3 -c "from inky.auto import auto; display = auto(); print(f'Detected: {display.width}x{display.height}')"
```

---

## Required System Dependencies

The Inky library requires these system packages (should already be installed on Raspberry Pi OS):

```bash
# Enable I2C and SPI (if not already enabled)
sudo raspi-config nonint do_i2c 0
sudo raspi-config nonint do_spi 0
```

---

## Restart Your Server

After installing the Inky library, restart your web server:

```bash
cd /home/lewsiafat/Documents/workspaceEink/myInky
pkill -f "uvicorn src.main:app"
uv run uvicorn src.main:app --host 0.0.0.0 --port 8000
```

The server will now detect the Inky library and use the real display instead of mock mode!

---

## Troubleshooting

### "No module named 'inky'"

Make sure you installed it in the same virtual environment:

```bash
cd /home/lewsiafat/Documents/workspaceEink/myInky
source .venv/bin/activate  # Activate venv
pip install -e ../inky     # Install inky library
```

Or with uv:

```bash
cd /home/lewsiafat/Documents/workspaceEink/myInky
uv pip install -e ../inky
```

### GPIO Permission Errors

Add your user to the gpio group:

```bash
sudo usermod -a -G gpio lewsiafat
sudo usermod -a -G spi lewsiafat
sudo usermod -a -G i2c lewsiafat
```

Then log out and log back in.

### Display Not Detected

Check if I2C and SPI are enabled:

```bash
ls /dev/i2c-* /dev/spidev*
```

You should see devices like `/dev/i2c-1` and `/dev/spidev0.0`.

---

## Quick Install Script

Here's a complete script to copy and install the Inky library:

```bash
#!/bin/bash
# Run this on your LOCAL machine

REMOTE_USER="lewsiafat"
REMOTE_HOST="192.168.31.90"

# Copy inky library to server
echo "Copying Inky library to server..."
scp -r ref_source/inky ${REMOTE_USER}@${REMOTE_HOST}:/home/lewsiafat/Documents/workspaceEink/

# Install on server
echo "Installing Inky library on server..."
ssh ${REMOTE_USER}@${REMOTE_HOST} << 'EOF'
cd /home/lewsiafat/Documents/workspaceEink/myInky
uv pip install -e ../inky
echo "Inky library installed!"
EOF

echo "Done! Restart your server to use the real display."
```

Save this as `install_inky.sh`, make it executable, and run it:

```bash
chmod +x install_inky.sh
./install_inky.sh
```
