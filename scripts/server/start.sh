#!/bin/bash
# Start InkyFrame server

echo "Starting InkyFrame server..."

# Check if server is already running
if pgrep -f "uvicorn src.main:app" > /dev/null; then
    echo "Server is already running!"
    echo "Use ./stop.sh to stop it first."
    exit 1
fi

# Load environment variables from .env if it exists
if [ -f .env ]; then
    echo "Loading environment variables from .env..."
    export $(cat .env | grep -v '^#' | xargs)
fi

# Start server in background
echo "Starting uvicorn server on port 8000..."
nohup uv run uvicorn src.main:app --host 0.0.0.0 --port 8000 > server.log 2>&1 &

# Get the PID
SERVER_PID=$!
echo $SERVER_PID > server.pid

# Wait a moment and check if it started successfully
sleep 2

if pgrep -f "uvicorn src.main:app" > /dev/null; then
    echo "✓ Server started successfully!"
    echo "  PID: $SERVER_PID"
    echo "  URL: http://0.0.0.0:8000"
    echo "  Log: server.log"
    echo ""
    echo "Use ./stop.sh to stop the server"
else
    echo "✗ Failed to start server. Check server.log for errors."
    exit 1
fi
