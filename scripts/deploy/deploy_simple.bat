@echo off
REM Simple deployment script - just upload code to server

REM Configuration - UPDATE THESE VALUES
set REMOTE_USER=lewsiafat
set REMOTE_HOST=192.168.31.90
set REMOTE_PATH=/home/lewsiafat/Documents/workspaceEink/myInky

echo Uploading code to server...
echo.

REM Create remote directories first
echo [0/6] Creating remote directories...
ssh %REMOTE_USER%@%REMOTE_HOST% "mkdir -p %REMOTE_PATH%/scripts/server"

REM Upload src directory
echo [1/6] Uploading src...
scp -r src %REMOTE_USER%@%REMOTE_HOST%:%REMOTE_PATH%/

REM Upload static directory
echo [2/6] Uploading static...
scp -r static %REMOTE_USER%@%REMOTE_HOST%:%REMOTE_PATH%/

REM Upload pyproject.toml
echo [3/6] Uploading pyproject.toml...
scp pyproject.toml %REMOTE_USER%@%REMOTE_HOST%:%REMOTE_PATH%/

REM Upload server management scripts
echo [4/6] Uploading server scripts...
scp scripts/server/start.sh scripts/server/stop.sh scripts/server/restart.sh scripts/server/status.sh %REMOTE_USER%@%REMOTE_HOST%:%REMOTE_PATH%/scripts/server/

:: REM Make scripts executable
:: echo [5/6] Making scripts executable...
:: ssh %REMOTE_USER%@%REMOTE_HOST% "chmod +x %REMOTE_PATH%/scripts/server/*.sh"

:: REM Upload .env if exists
:: echo [6/6] Uploading .env (if exists)...
:: if exist .env (
::     scp .env %REMOTE_USER%@%REMOTE_HOST%:%REMOTE_PATH%/
::     echo .env uploaded - Weather API key configured!
:: ) else (
::     echo WARNING: .env not found! Weather feature will not work.
::     echo Create .env file with OPENWEATHER_API_KEY before deploying.
:: )

echo.
echo ========================================
echo   Upload Complete!
echo ========================================
echo.
echo Next: SSH into server and restart:
echo   ssh %REMOTE_USER%@%REMOTE_HOST%
echo   cd %REMOTE_PATH%
echo   scripts/server/restart.sh
echo.
pause
