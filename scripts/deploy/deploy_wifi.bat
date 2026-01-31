@echo off
REM Deploy WiFi App components

REM Configuration
set REMOTE_USER=lewsiafat
set REMOTE_HOST=192.168.31.90
set REMOTE_PATH=/home/lewsiafat/Documents/workspaceEink/myInky

echo Uploading WiFi App components...
echo.

REM 1. Create remote directories
echo [1/5] Creating remote directories...
ssh %REMOTE_USER%@%REMOTE_HOST% "mkdir -p %REMOTE_PATH%/scripts/wifi %REMOTE_PATH%/scripts/services"

REM 2. Upload src directory (this includes wifi_app)
echo [2/5] Uploading src...
scp -r src %REMOTE_USER%@%REMOTE_HOST%:%REMOTE_PATH%/

REM 3. Upload wifi scripts
echo [3/5] Uploading wifi scripts...
scp scripts/wifi/button_monitor.py scripts/wifi/start_wifi_app.sh scripts/wifi/install_wifi.sh %REMOTE_USER%@%REMOTE_HOST%:%REMOTE_PATH%/scripts/wifi/

REM 4. Upload service files
echo [4/5] Uploading service files...
scp scripts/services/inky-wifi.service scripts/services/inky-monitor.service %REMOTE_USER%@%REMOTE_HOST%:%REMOTE_PATH%/scripts/services/

REM 5. Make scripts executable
echo [5/5] Making scripts executable...
ssh %REMOTE_USER%@%REMOTE_HOST% "chmod +x %REMOTE_PATH%/scripts/wifi/*.sh"

echo.
echo ========================================
echo   Deployment Complete!
echo ========================================
echo.
echo To finish installation, run on server:
echo   ssh %REMOTE_USER%@%REMOTE_HOST%
echo   cd %REMOTE_PATH%
echo   ./scripts/wifi/install_wifi.sh
echo.
pause
