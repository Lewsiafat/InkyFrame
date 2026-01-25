@echo off
REM Simple deployment script - just upload code to server

REM Configuration - UPDATE THESE VALUES
set REMOTE_USER=lewsiafat
set REMOTE_HOST=192.168.31.90
set REMOTE_PATH=/home/lewsiafat/Documents/workspaceEink/myInky

echo Uploading code to server...
echo.

REM Upload src directory
echo [1/5] Uploading src...
scp -r src %REMOTE_USER%@%REMOTE_HOST%:%REMOTE_PATH%/

REM Upload static directory
echo [2/5] Uploading static...
scp -r static %REMOTE_USER%@%REMOTE_HOST%:%REMOTE_PATH%/

REM Upload pyproject.toml
echo [3/5] Uploading pyproject.toml...
scp pyproject.toml %REMOTE_USER%@%REMOTE_HOST%:%REMOTE_PATH%/

REM Upload server management scripts
echo [4/5] Uploading server scripts...
scp scripts/server/start.sh scripts/server/stop.sh scripts/server/restart.sh scripts/server/status.sh %REMOTE_USER%@%REMOTE_HOST%:%REMOTE_PATH%/scripts/server/

REM Upload .env if exists
echo [5/5] Uploading .env (if exists)...
if exist .env (
    scp .env %REMOTE_USER%@%REMOTE_HOST%:%REMOTE_PATH%/
    echo .env uploaded
) else (
    echo .env not found, skipping
)

echo.
echo ========================================
echo   Upload Complete!
echo ========================================
echo.
echo Next: SSH into server and restart:
echo   ssh %REMOTE_USER%@%REMOTE_HOST%
echo   cd %REMOTE_PATH%
echo   chmod +x scripts/server/*.sh
echo   scripts/server/restart.sh
echo.
pause
