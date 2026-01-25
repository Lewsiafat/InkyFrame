# Deployment Scripts

InkyFrame includes multiple deployment scripts for different use cases.

## Quick Deploy (Recommended)

### Windows
```cmd
deploy_simple.bat
```

### Linux/Mac
```bash
chmod +x deploy_simple.sh
./deploy_simple.sh
```

**What it does:**
- Uploads `src/` directory
- Uploads `static/` directory  
- Uploads `pyproject.toml`
- Uploads server management scripts (start.sh, stop.sh, etc.)
- Uploads `.env` file (if exists)

**After deployment:**
```bash
ssh YOUR_USERNAME@YOUR_SERVER_IP
cd /path/to/InkyFrame
chmod +x *.sh
./restart.sh
```

## Full Deploy (Advanced)

### Linux/Mac
```bash
chmod +x deploy.sh
./deploy.sh
```

**What it does:**
- Checks SSH connection
- Creates remote directories
- Syncs all files using rsync (excludes .git, __pycache__, etc.)
- Installs dependencies with `uv sync`
- Creates upload directories
- Stops existing server

**After deployment:**
```bash
ssh YOUR_USERNAME@YOUR_SERVER_IP
cd /path/to/InkyFrame
./start.sh
```

## Configuration

Before using deployment scripts, update these variables:

**deploy_simple.bat / deploy_simple.sh:**
```bash
REMOTE_USER="YOUR_USERNAME"
REMOTE_HOST="YOUR_SERVER_IP"
REMOTE_PATH="/path/to/InkyFrame"
```

**deploy.sh:**
```bash
REMOTE_USER="YOUR_USERNAME"
REMOTE_HOST="YOUR_SERVER_IP"
REMOTE_PATH="/path/to/InkyFrame"
```

## Server Management

After deployment, use these scripts on the server:

```bash
./start.sh      # Start server in background
./stop.sh       # Stop server
./restart.sh    # Restart server
./status.sh     # Check server status
```

## Troubleshooting

**Permission denied:**
```bash
chmod +x deploy_simple.sh deploy.sh
```

**SSH password prompt:**
- Set up SSH key authentication for passwordless login
- Or use `ssh-copy-id YOUR_USERNAME@YOUR_SERVER_IP`

**Connection refused:**
- Check network connection
- Verify server IP address
- Ensure SSH is enabled on server

**Files not uploading:**
- Check file paths
- Verify remote directory exists
- Check disk space on server
