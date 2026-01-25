# Deployment script for Inky Photo Display Web Server (PowerShell)
# Deploys to development board via SSH

# Configuration
$REMOTE_USER = "YOUR_USERNAME"
$REMOTE_HOST = "192.168.31.90"
$REMOTE_PATH = "/home/pi/Documents/workspaceEink/myInky"
$LOCAL_PATH = "."

Write-Host "=== Inky Photo Display Deployment ===" -ForegroundColor Green
Write-Host ""

# Check if SSH is available
Write-Host "[1/6] Checking SSH connection..." -ForegroundColor Yellow
try {
    $result = ssh -o ConnectTimeout=5 ${REMOTE_USER}@${REMOTE_HOST} "echo 'Connection successful'" 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "SSH connection failed"
    }
    Write-Host "✓ SSH connection successful" -ForegroundColor Green
} catch {
    Write-Host "Error: Cannot connect to ${REMOTE_USER}@${REMOTE_HOST}" -ForegroundColor Red
    Write-Host "Please check:"
    Write-Host "  - Network connection"
    Write-Host "  - SSH credentials"
    Write-Host "  - Remote host is accessible"
    exit 1
}
Write-Host ""

# Create remote directory
Write-Host "[2/6] Creating remote directory..." -ForegroundColor Yellow
ssh ${REMOTE_USER}@${REMOTE_HOST} "mkdir -p ${REMOTE_PATH}"
Write-Host "✓ Remote directory ready" -ForegroundColor Green
Write-Host ""

# Sync files using scp (since rsync might not be available on Windows)
Write-Host "[3/6] Syncing files to remote server..." -ForegroundColor Yellow
Write-Host "Note: Using scp for file transfer. For faster sync, install rsync and use deploy.sh" -ForegroundColor Cyan

# Create a temporary exclude list
$excludeItems = @(
    ".git",
    "__pycache__",
    "*.pyc",
    ".venv",
    "venv",
    "uploads",
    ".vscode",
    ".idea",
    "*.log",
    "ref_source"
)

# Use scp to copy files
scp -r -o "ConnectTimeout=10" `
    ${LOCAL_PATH}/src `
    ${LOCAL_PATH}/static `
    ${LOCAL_PATH}/spec `
    ${LOCAL_PATH}/pyproject.toml `
    ${LOCAL_PATH}/README.md `
    ${LOCAL_PATH}/.gitignore `
    ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_PATH}/

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: File sync failed" -ForegroundColor Red
    exit 1
}
Write-Host "✓ Files synced successfully" -ForegroundColor Green
Write-Host ""

# Install dependencies on remote server
Write-Host "[4/6] Installing dependencies on remote server..." -ForegroundColor Yellow
ssh ${REMOTE_USER}@${REMOTE_HOST} "cd ${REMOTE_PATH} && uv sync"
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Dependency installation failed" -ForegroundColor Red
    exit 1
}
Write-Host "✓ Dependencies installed" -ForegroundColor Green
Write-Host ""

# Create upload directories
Write-Host "[5/6] Creating upload directories..." -ForegroundColor Yellow
ssh ${REMOTE_USER}@${REMOTE_HOST} "cd ${REMOTE_PATH} && mkdir -p uploads/originals uploads/optimized uploads/thumbnails"
Write-Host "✓ Upload directories created" -ForegroundColor Green
Write-Host ""

# Check if server is already running and stop it
Write-Host "[6/6] Managing server process..." -ForegroundColor Yellow
ssh ${REMOTE_USER}@${REMOTE_HOST} "pkill -f 'uvicorn src.main:app' || true"
Write-Host "✓ Stopped existing server (if any)" -ForegroundColor Green
Write-Host ""

Write-Host "=== Deployment Complete ===" -ForegroundColor Green
Write-Host ""
Write-Host "To start the server on the remote machine, run:"
Write-Host "ssh ${REMOTE_USER}@${REMOTE_HOST} 'cd ${REMOTE_PATH} && uv run uvicorn src.main:app --host 0.0.0.0 --port 8000'" -ForegroundColor Yellow
Write-Host ""
Write-Host "Or to run in background:"
Write-Host "ssh ${REMOTE_USER}@${REMOTE_HOST} 'cd ${REMOTE_PATH} && nohup uv run uvicorn src.main:app --host 0.0.0.0 --port 8000 > server.log 2>&1 &'" -ForegroundColor Yellow
Write-Host ""
Write-Host "Access the web interface at:"
Write-Host "http://192.168.31.90:8000" -ForegroundColor Green
