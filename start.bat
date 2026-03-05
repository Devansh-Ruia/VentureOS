@echo off
echo ========================================
echo VentureOS Startup Script
echo ========================================
echo.

REM Check if .env exists
if not exist "backend\.env" (
    echo [ERROR] backend\.env file not found!
    echo Please copy .env.example to backend\.env and add your API keys.
    echo.
    echo Run: copy .env.example backend\.env
    echo.
    pause
    exit /b 1
)

echo [1/2] Starting Backend (FastAPI)...
start "VentureOS Backend" cmd /k "cd backend && uvicorn main:app --reload --port 8000"

timeout /t 3 /nobreak >nul

echo [2/2] Starting Frontend (Next.js)...
start "VentureOS Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ========================================
echo VentureOS is starting!
echo ========================================
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Press any key to close this window...
pause >nul
