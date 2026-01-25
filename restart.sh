#!/bin/bash
# Restart InkyFrame server

echo "Restarting InkyFrame server..."

# Stop the server
./stop.sh

# Wait a moment
sleep 2

# Start the server
./start.sh
