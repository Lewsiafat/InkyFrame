#!/bin/bash

# Navigate to project root
cd "$(dirname "$0")/../.."

# Activate environment and run app
# Using port 8000. Supervisor ensures main app is stopped so port is free.
# Using '0.0.0.0' to be accessible via Hotspot IP
/home/lewsiafat/.local/bin/uv run uvicorn src.wifi_app.main:app --host 0.0.0.0 --port 8000
