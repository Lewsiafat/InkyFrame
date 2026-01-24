@echo off
REM Deployment script for Inky Photo Display Web Server (Windows Batch)
REM Deploys to development board via SSH using rsync

setlocal enabledelayedexpansion

REM Configuration
set REMOTE_USER=YOUR_USERNAME
set REMOTE_HOST=192.168.31.90
set REMOTE_PATH=/home/pi/Documents/workspaceEink/myInky
set LOCAL_PATH=.

echo ========================================
echo   Inky Photo Display Deployment
echo ========================================
echo.

REM Check if rsync is available
where rsync >nul 2>&1
if errorlevel 1 (
    echo [WARNING] rsync not found. Install rsync for faster deployment.
    echo You can install it via: winget install rsync
    echo.
    echo Falling back to scp...
    set USE_SCP=1
) else (
    set USE_SCP=0
)

REM Check if SSH is available
echo [1/3] Checking SSH connection...
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
echo [2/3] Creating remote directory...
ssh %REMOTE_USER%@%REMOTE_HOST% "mkdir -p %REMOTE_PATH%"
echo [OK] Remote directory ready
echo.

REM Sync files
echo [3/3] Syncing files to remote server...
echo This may take a few minutes...

if %USE_SCP%==1 (
    REM Use scp as fallback
    scp -r src %REMOTE_USER%@%REMOTE_HOST%:%REMOTE_PATH%/
    scp -r static %REMOTE_USER%@%REMOTE_HOST%:%REMOTE_PATH%/
    scp -r spec %REMOTE_USER%@%REMOTE_HOST%:%REMOTE_PATH%/
    scp pyproject.toml %REMOTE_USER%@%REMOTE_HOST%:%REMOTE_PATH%/
    scp README.md %REMOTE_USER%@%REMOTE_HOST%:%REMOTE_PATH%/
    scp .gitignore %REMOTE_USER%@%REMOTE_HOST%:%REMOTE_PATH%/
    scp DEPLOYMENT.md %REMOTE_USER%@%REMOTE_HOST%:%REMOTE_PATH%/
) else (
    REM Use rsync for faster sync
    rsync -avz --progress --exclude=".git" --exclude="__pycache__" --exclude="*.pyc" --exclude=".venv" --exclude="venv" --exclude="uploads/*" --exclude=".vscode" --exclude=".idea" --exclude="*.log" --exclude="ref_source" -e ssh %LOCAL_PATH%/ %REMOTE_USER%@%REMOTE_HOST%:%REMOTE_PATH%/
)

if errorlevel 1 (
    echo [ERROR] File sync failed
    pause
    exit /b 1
)
echo [OK] Files synced successfully
echo.

echo ========================================
echo   Deployment Complete!
echo ========================================
echo.
echo Files have been transferred to the server.
echo.
echo NEXT STEPS - Run these commands on the server:
echo --------------------------------------------------------
echo 1. SSH into the server:
echo    ssh %REMOTE_USER%@%REMOTE_HOST%
echo.
echo 2. Navigate to project directory:
echo    cd %REMOTE_PATH%
echo.
echo 3. Install uv (if not already installed):
echo    curl -LsSf https://astral.sh/uv/install.sh ^| sh
echo    source $HOME/.cargo/env
echo.
echo 4. Install dependencies:
echo    uv sync
echo.
echo 5. Create upload directories:
echo    mkdir -p uploads/originals uploads/optimized uploads/thumbnails
echo.
echo 6. Start the server:
echo    uv run uvicorn src.main:app --host 0.0.0.0 --port 8000
echo.
echo Or run in background:
echo    nohup uv run uvicorn src.main:app --host 0.0.0.0 --port 8000 ^> server.log 2^>^&1 ^&
echo.
echo Access the web interface at:
echo http://192.168.31.90:8000
echo --------------------------------------------------------
echo.
echo See DEPLOYMENT.md for detailed instructions.
echo.
pause

