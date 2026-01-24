#!/bin/bash
# Deployment script for Inky Photo Display Web Server
# Deploys to development board via SSH

# Configuration
REMOTE_USER="YOUR_USERNAME"
REMOTE_HOST="192.168.31.90"
REMOTE_PATH="/home/pi/Documents/workspaceEink/myInky"
LOCAL_PATH="."

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== Inky Photo Display Deployment ===${NC}"
echo ""

# Check if SSH connection is available
echo -e "${YELLOW}[1/6] Checking SSH connection...${NC}"
if ! ssh -o ConnectTimeout=5 ${REMOTE_USER}@${REMOTE_HOST} "echo 'Connection successful'" > /dev/null 2>&1; then
    echo -e "${RED}Error: Cannot connect to ${REMOTE_USER}@${REMOTE_HOST}${NC}"
    echo "Please check:"
    echo "  - Network connection"
    echo "  - SSH credentials"
    echo "  - Remote host is accessible"
    exit 1
fi
echo -e "${GREEN}✓ SSH connection successful${NC}"
echo ""

# Create remote directory if it doesn't exist
echo -e "${YELLOW}[2/6] Creating remote directory...${NC}"
ssh ${REMOTE_USER}@${REMOTE_HOST} "mkdir -p ${REMOTE_PATH}"
echo -e "${GREEN}✓ Remote directory ready${NC}"
echo ""

# Sync files using rsync (excludes .git, __pycache__, uploads, .venv)
echo -e "${YELLOW}[3/6] Syncing files to remote server...${NC}"
rsync -avz --progress \
    --exclude='.git' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='.venv' \
    --exclude='venv' \
    --exclude='uploads/*' \
    --exclude='.vscode' \
    --exclude='.idea' \
    --exclude='*.log' \
    --exclude='ref_source' \
    ${LOCAL_PATH}/ ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_PATH}/

if [ $? -ne 0 ]; then
    echo -e "${RED}Error: File sync failed${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Files synced successfully${NC}"
echo ""

# Install dependencies on remote server
echo -e "${YELLOW}[4/6] Installing dependencies on remote server...${NC}"
ssh ${REMOTE_USER}@${REMOTE_HOST} "cd ${REMOTE_PATH} && uv sync"
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Dependency installation failed${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Dependencies installed${NC}"
echo ""

# Create upload directories
echo -e "${YELLOW}[5/6] Creating upload directories...${NC}"
ssh ${REMOTE_USER}@${REMOTE_HOST} "cd ${REMOTE_PATH} && mkdir -p uploads/originals uploads/optimized uploads/thumbnails"
echo -e "${GREEN}✓ Upload directories created${NC}"
echo ""

# Check if server is already running and stop it
echo -e "${YELLOW}[6/6] Managing server process...${NC}"
ssh ${REMOTE_USER}@${REMOTE_HOST} "pkill -f 'uvicorn src.main:app' || true"
echo -e "${GREEN}✓ Stopped existing server (if any)${NC}"
echo ""

echo -e "${GREEN}=== Deployment Complete ===${NC}"
echo ""
echo "To start the server on the remote machine, run:"
echo -e "${YELLOW}ssh ${REMOTE_USER}@${REMOTE_HOST} 'cd ${REMOTE_PATH} && uv run uvicorn src.main:app --host 0.0.0.0 --port 8000'${NC}"
echo ""
echo "Or to run in background:"
echo -e "${YELLOW}ssh ${REMOTE_USER}@${REMOTE_HOST} 'cd ${REMOTE_PATH} && nohup uv run uvicorn src.main:app --host 0.0.0.0 --port 8000 > server.log 2>&1 &'${NC}"
echo ""
echo "Access the web interface at:"
echo -e "${GREEN}http://192.168.31.90:8000${NC}"
