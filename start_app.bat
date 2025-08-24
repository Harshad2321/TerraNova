@echo off
echo Starting TerraNova Application...
echo.

echo 1. Starting Backend Server...
cd backend
start "TerraNova Backend" cmd /k "uvicorn main:app --reload --host 127.0.0.1 --port 8000"

echo 2. Waiting for backend to start...
timeout /t 3 /nobreak >nul

echo 3. Opening Frontend in Browser...
cd ..\frontend
start "" "index.html"

echo.
echo ✅ TerraNova is now running!
echo Backend: http://127.0.0.1:8000
echo Frontend: Opening in your default browser
echo.
echo Press any key to exit...
pause >nul
