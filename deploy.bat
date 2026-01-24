@echo off
REM Deployment script for Inky Photo Display Web Server (Windows Batch)
REM Deploys to development board via SSH

setlocal enabledelayedexpansion

REM Configuration
set REMOTE_USER=lewsiafat
set REMOTE_HOST=192.168.31.90
set REMOTE_PATH=/home/lewsiafat/Documents/workspaceEink/myInky
set LOCAL_PATH=.

echo ========================================
echo   Inky Photo Display Deployment
echo ========================================
echo.

REM Check if SSH is available
echo [1/6] Checking SSH connection...
ssh -o ConnectTimeout=5 %REMOTE_USER%@%REMOTE_HOST% "echo Connection successful" >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Cannot connect to %REMOTE_USER%@%REMOTE_HOST%
    echo Please check:
    echo   - Network connection
    echo   - SSH credentials
    echo   - Remote host is accessible
    pause
    exit /b 1
)
echo [OK] SSH connection successful
echo.

REM Create remote directory
echo [2/6] Creating remote directory...
ssh %REMOTE_USER%@%REMOTE_HOST% "mkdir -p %REMOTE_PATH%"
echo [OK] Remote directory ready
echo.

REM Sync files using scp
echo [3/6] Syncing files to remote server...
echo This may take a few minutes...

REM Copy directories
scp -r src %REMOTE_USER%@%REMOTE_HOST%:%REMOTE_PATH%/
scp -r static %REMOTE_USER%@%REMOTE_HOST%:%REMOTE_PATH%/
scp -r spec %REMOTE_USER%@%REMOTE_HOST%:%REMOTE_PATH%/

REM Copy individual files
scp pyproject.toml %REMOTE_USER%@%REMOTE_HOST%:%REMOTE_PATH%/
scp README.md %REMOTE_USER%@%REMOTE_HOST%:%REMOTE_PATH%/
scp .gitignore %REMOTE_USER%@%REMOTE_HOST%:%REMOTE_PATH%/
scp DEPLOYMENT.md %REMOTE_USER%@%REMOTE_HOST%:%REMOTE_PATH%/

if errorlevel 1 (
    echo [ERROR] File sync failed
    pause
    exit /b 1
)
echo [OK] Files synced successfully
echo.

REM Install dependencies on remote server
echo [4/6] Installing dependencies on remote server...
echo This may take a few minutes...
ssh %REMOTE_USER%@%REMOTE_HOST% "cd %REMOTE_PATH% && uv sync"
if errorlevel 1 (
    echo [ERROR] Dependency installation failed
    pause
    exit /b 1
)
echo [OK] Dependencies installed
echo.

REM Create upload directories
echo [5/6] Creating upload directories...
ssh %REMOTE_USER%@%REMOTE_HOST% "cd %REMOTE_PATH% && mkdir -p uploads/originals uploads/optimized uploads/thumbnails"
echo [OK] Upload directories created
echo.

REM Stop existing server
echo [6/6] Managing server process...
ssh %REMOTE_USER%@%REMOTE_HOST% "pkill -f 'uvicorn src.main:app' || true"
echo [OK] Stopped existing server (if any)
echo.

echo ========================================
echo   Deployment Complete!
echo ========================================
echo.
echo To start the server on the remote machine, run:
echo ssh %REMOTE_USER%@%REMOTE_HOST% "cd %REMOTE_PATH% && uv run uvicorn src.main:app --host 0.0.0.0 --port 8000"
echo.
echo Or to run in background:
echo ssh %REMOTE_USER%@%REMOTE_HOST% "cd %REMOTE_PATH% && nohup uv run uvicorn src.main:app --host 0.0.0.0 --port 8000 > server.log 2>&1 &"
echo.
echo Access the web interface at:
echo http://192.168.31.90:8000
echo.
pause
