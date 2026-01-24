# Deployment Guide

## Quick Deploy

### Windows (PowerShell)
```powershell
.\deploy.ps1
```

### Linux/Mac (Bash)
```bash
chmod +x deploy.sh
./deploy.sh
```

---

## What the Script Does

1. **Checks SSH Connection** - Verifies connectivity to the remote server
2. **Creates Remote Directory** - Ensures deployment path exists
3. **Syncs Files** - Transfers project files (excludes .git, uploads, cache)
4. **Installs Dependencies** - Runs `uv sync` on remote server
5. **Creates Upload Directories** - Sets up storage folders
6. **Stops Existing Server** - Kills any running server process

---

## Manual Deployment

If you prefer to deploy manually:

### 1. Copy Files
```bash
scp -r src static spec pyproject.toml README.md lewsiafat@192.168.31.90:/home/lewsiafat/Documents/workspaceEink/myInky/
```

### 2. SSH into Server
```bash
ssh lewsiafat@192.168.31.90
```

### 3. Navigate to Project
```bash
cd /home/lewsiafat/Documents/workspaceEink/myInky
```

### 4. Install Dependencies
```bash
uv sync
```

### 5. Create Upload Directories
```bash
mkdir -p uploads/originals uploads/optimized uploads/thumbnails
```

### 6. Start Server
```bash
uv run uvicorn src.main:app --host 0.0.0.0 --port 8000
```

---

## Starting the Server

### Foreground (for testing)
```bash
ssh lewsiafat@192.168.31.90 'cd /home/lewsiafat/Documents/workspaceEink/myInky && uv run uvicorn src.main:app --host 0.0.0.0 --port 8000'
```

### Background (persistent)
```bash
ssh lewsiafat@192.168.31.90 'cd /home/lewsiafat/Documents/workspaceEink/myInky && nohup uv run uvicorn src.main:app --host 0.0.0.0 --port 8000 > server.log 2>&1 &'
```

### Check Server Status
```bash
ssh lewsiafat@192.168.31.90 'ps aux | grep uvicorn'
```

### Stop Server
```bash
ssh lewsiafat@192.168.31.90 'pkill -f "uvicorn src.main:app"'
```

### View Logs
```bash
ssh lewsiafat@192.168.31.90 'tail -f /home/lewsiafat/Documents/workspaceEink/myInky/server.log'
```

---

## Access the Application

After deployment, access the web interface at:

**http://192.168.31.90:8000**

---

## Systemd Service (Optional)

For automatic startup on boot, create a systemd service:

### 1. Create Service File
```bash
ssh lewsiafat@192.168.31.90 'sudo nano /etc/systemd/system/inky-server.service'
```

### 2. Add Configuration
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

[Install]
WantedBy=multi-user.target
```

### 3. Enable and Start Service
```bash
ssh lewsiafat@192.168.31.90 'sudo systemctl daemon-reload'
ssh lewsiafat@192.168.31.90 'sudo systemctl enable inky-server'
ssh lewsiafat@192.168.31.90 'sudo systemctl start inky-server'
```

### 4. Check Service Status
```bash
ssh lewsiafat@192.168.31.90 'sudo systemctl status inky-server'
```

---

## Troubleshooting

### SSH Connection Issues
- Verify network connectivity: `ping 192.168.31.90`
- Check SSH service: `ssh lewsiafat@192.168.31.90 'systemctl status sshd'`
- Verify credentials

### Deployment Fails
- Check disk space: `ssh lewsiafat@192.168.31.90 'df -h'`
- Verify `uv` is installed: `ssh lewsiafat@192.168.31.90 'which uv'`
- Check permissions on remote directory

### Server Won't Start
- Check if port 8000 is in use: `ssh lewsiafat@192.168.31.90 'lsof -i :8000'`
- View error logs: `ssh lewsiafat@192.168.31.90 'cat /home/lewsiafat/Documents/workspaceEink/myInky/server.log'`
- Verify Python version: `ssh lewsiafat@192.168.31.90 'python3 --version'`

### Inky Display Not Working
- Check if running on Raspberry Pi or compatible board
- Verify Inky library is installed
- Check GPIO permissions
- Review display controller logs

---

## Environment Variables

Set environment variables on the remote server:

```bash
ssh lewsiafat@192.168.31.90 'cd /home/lewsiafat/Documents/workspaceEink/myInky && echo "export PORT=8000" >> ~/.bashrc'
```

Available variables:
- `HOST` - Server host (default: 0.0.0.0)
- `PORT` - Server port (default: 8000)
- `INKY_MODEL` - Display model (default: auto)

---

## Security Considerations

### Production Deployment
1. **Use HTTPS** - Set up nginx with SSL/TLS
2. **Firewall** - Configure firewall rules
3. **Authentication** - Add user authentication if needed
4. **CORS** - Restrict allowed origins in production
5. **File Size Limits** - Adjust based on requirements

### Example nginx Configuration
```nginx
server {
    listen 80;
    server_name 192.168.31.90;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

---

## Quick Reference

| Action | Command |
|--------|---------|
| Deploy | `./deploy.ps1` or `./deploy.sh` |
| Start Server | `ssh lewsiafat@192.168.31.90 'cd /home/lewsiafat/Documents/workspaceEink/myInky && uv run uvicorn src.main:app --host 0.0.0.0 --port 8000'` |
| Stop Server | `ssh lewsiafat@192.168.31.90 'pkill -f uvicorn'` |
| View Logs | `ssh lewsiafat@192.168.31.90 'tail -f /home/lewsiafat/Documents/workspaceEink/myInky/server.log'` |
| Check Status | `ssh lewsiafat@192.168.31.90 'ps aux \| grep uvicorn'` |
| Access UI | http://192.168.31.90:8000 |
