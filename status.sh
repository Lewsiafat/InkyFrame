#!/bin/bash
# Check InkyFrame server status

if pgrep -f "uvicorn src.main:app" > /dev/null; then
    PID=$(pgrep -f "uvicorn src.main:app")
    echo "✓ Server is RUNNING"
    echo "  PID: $PID"
    echo "  URL: http://0.0.0.0:8000"
    
    if [ -f server.pid ]; then
        SAVED_PID=$(cat server.pid)
        if [ "$PID" == "$SAVED_PID" ]; then
            echo "  PID file: ✓ matches"
        else
            echo "  PID file: ✗ mismatch (saved: $SAVED_PID)"
        fi
    else
        echo "  PID file: ✗ missing"
    fi
    
    if [ -f server.log ]; then
        echo "  Log file: server.log"
        echo ""
        echo "Last 5 log lines:"
        tail -5 server.log
    fi
else
    echo "✗ Server is NOT running"
    
    if [ -f server.log ]; then
        echo ""
        echo "Last error from log:"
        tail -10 server.log | grep -i error || echo "No errors found in log"
    fi
fi
