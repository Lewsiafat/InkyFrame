#!/bin/bash
# Install Inky library on remote server
# Run this script from your local machine

REMOTE_USER="lewsiafat"
REMOTE_HOST="192.168.31.90"
REMOTE_BASE="/home/lewsiafat/Documents/workspaceEink"

echo "========================================="
echo "  Installing Inky Library on Server"
echo "========================================="
echo ""

# Check if ref_source/inky exists
if [ ! -d "ref_source/inky" ]; then
    echo "[ERROR] ref_source/inky directory not found!"
    echo "Please run this script from the project root directory."
    exit 1
fi

# Copy inky library to server
echo "[1/2] Copying Inky library to server..."
scp -r ref_source/inky ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_BASE}/

if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to copy Inky library"
    exit 1
fi
echo "[OK] Inky library copied"
echo ""

# Install on server
echo "[2/2] Installing Inky library on server..."
ssh ${REMOTE_USER}@${REMOTE_HOST} << EOF
cd ${REMOTE_BASE}/myInky
echo "Installing Inky library..."
uv pip install -e ../inky
if [ \$? -eq 0 ]; then
    echo "Inky library installed successfully!"
else
    echo "Failed to install Inky library"
    exit 1
fi
EOF

if [ $? -ne 0 ]; then
    echo "[ERROR] Installation failed"
    exit 1
fi

echo ""
echo "========================================="
echo "  Installation Complete!"
echo "========================================="
echo ""
echo "Next steps:"
echo "1. Restart your server:"
echo "   ssh ${REMOTE_USER}@${REMOTE_HOST} 'cd ${REMOTE_BASE}/myInky && pkill -f uvicorn && uv run uvicorn src.main:app --host 0.0.0.0 --port 8000'"
echo ""
echo "2. The server will now use the real Inky display!"
echo ""
