@echo off
REM Simple deployment script - just upload code to server

set REMOTE_USER=lewsiafat
set REMOTE_HOST=192.168.31.90
set REMOTE_PATH=/home/lewsiafat/Documents/workspaceEink/myInky

echo Uploading code to server...
echo.

REM Upload src directory
echo [1/4] Uploading src...
scp -r src %REMOTE_USER%@%REMOTE_HOST%:%REMOTE_PATH%/

REM Upload static directory
echo [2/4] Uploading static...
scp -r static %REMOTE_USER%@%REMOTE_HOST%:%REMOTE_PATH%/

REM Upload pyproject.toml
echo [3/4] Uploading pyproject.toml...
scp pyproject.toml %REMOTE_USER%@%REMOTE_HOST%:%REMOTE_PATH%/

REM Upload .env if exists
echo [4/4] Uploading .env (if exists)...
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
echo   pkill -f uvicorn
echo   uv run uvicorn src.main:app --host 0.0.0.0 --port 8000
echo.
pause
