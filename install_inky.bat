@echo off
REM Install Inky library on remote server
REM Run this script from your local machine

set REMOTE_USER=YOUR_USERNAME
set REMOTE_HOST=192.168.31.90
set REMOTE_BASE=/home/pi/Documents/workspaceEink

echo =========================================
echo   Installing Inky Library on Server
echo =========================================
echo.

REM Check if ref_source\inky exists
if not exist "ref_source\inky" (
    echo [ERROR] ref_source\inky directory not found!
    echo Please run this script from the project root directory.
    pause
    exit /b 1
)

REM Copy inky library to server
echo [1/2] Copying Inky library to server...
scp -r ref_source/inky %REMOTE_USER%@%REMOTE_HOST%:%REMOTE_BASE%/

if errorlevel 1 (
    echo [ERROR] Failed to copy Inky library
    pause
    exit /b 1
)
echo [OK] Inky library copied
echo.

REM Install on server
echo [2/2] Installing Inky library on server...
ssh %REMOTE_USER%@%REMOTE_HOST% "cd %REMOTE_BASE%/myInky && uv pip install -e ../inky"

if errorlevel 1 (
    echo [ERROR] Installation failed
    pause
    exit /b 1
)

echo.
echo =========================================
echo   Installation Complete!
echo =========================================
echo.
echo Next steps:
echo 1. Restart your server:
echo    ssh %REMOTE_USER%@%REMOTE_HOST% "cd %REMOTE_BASE%/myInky && pkill -f uvicorn && uv run uvicorn src.main:app --host 0.0.0.0 --port 8000"
echo.
echo 2. The server will now use the real Inky display!
echo.
pause
