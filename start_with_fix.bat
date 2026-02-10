@echo off
REM Auto-fix script for Neon PostgreSQL registration issues
echo Applying permanent fix for Neon PostgreSQL registration...

REM Navigate to the project directory
cd /d "%~dp0"

REM Run the fix script
python neon_registration_fix.py

echo.
echo Starting the backend server...
REM Start the backend server
cd backend
uvicorn src.main:app --host 127.0.0.1 --port 8000
