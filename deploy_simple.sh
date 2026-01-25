#!/bin/bash
# Simple deployment script - just upload code to server

# Configuration - UPDATE THESE VALUES
REMOTE_USER="YOUR_USERNAME"
REMOTE_HOST="YOUR_SERVER_IP"
REMOTE_PATH="/path/to/InkyFrame"

echo "Uploading code to server..."
echo ""

# Upload src directory
echo "[1/5] Uploading src..."
scp -r src ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_PATH}/

# Upload static directory
echo "[2/5] Uploading static..."
scp -r static ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_PATH}/

# Upload pyproject.toml
echo "[3/5] Uploading pyproject.toml..."
scp pyproject.toml ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_PATH}/

# Upload server management scripts
echo "[4/5] Uploading server scripts..."
scp start.sh stop.sh restart.sh status.sh ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_PATH}/

# Upload .env if exists
echo "[5/5] Uploading .env (if exists)..."
if [ -f .env ]; then
    scp .env ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_PATH}/
    echo ".env uploaded"
else
    echo ".env not found, skipping"
fi

echo ""
echo "========================================"
echo "  Upload Complete!"
echo "========================================"
echo ""
echo "Next: SSH into server and restart:"
echo "  ssh ${REMOTE_USER}@${REMOTE_HOST}"
echo "  cd ${REMOTE_PATH}"
echo "  chmod +x *.sh"
echo "  ./restart.sh"
echo ""
