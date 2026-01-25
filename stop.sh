#!/bin/bash
# Stop InkyFrame server

echo "Stopping InkyFrame server..."

# Try to stop using PID file first
if [ -f server.pid ]; then
    PID=$(cat server.pid)
    if ps -p $PID > /dev/null 2>&1; then
        echo "Stopping server (PID: $PID)..."
        kill $PID
        sleep 1
        
        # Force kill if still running
        if ps -p $PID > /dev/null 2>&1; then
            echo "Force stopping server..."
            kill -9 $PID
        fi
        
        rm server.pid
        echo "✓ Server stopped successfully"
        exit 0
    else
        echo "PID file exists but process is not running"
        rm server.pid
    fi
fi

# Fallback: kill all uvicorn processes for this app
if pgrep -f "uvicorn src.main:app" > /dev/null; then
    echo "Stopping all InkyFrame server processes..."
    pkill -f "uvicorn src.main:app"
    sleep 1
    
    # Force kill if still running
    if pgrep -f "uvicorn src.main:app" > /dev/null; then
        echo "Force stopping..."
        pkill -9 -f "uvicorn src.main:app"
    fi
    
    echo "✓ Server stopped successfully"
else
    echo "Server is not running"
fi
