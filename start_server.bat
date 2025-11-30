@echo off
echo Starting AI Reel Generator Server...
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if .env exists
if not exist .env (
    echo ERROR: .env file not found!
    echo Please run setup_windows.bat first or create .env manually
    pause
    exit /b 1
)

REM Start Django server
echo Server starting at http://localhost:8000
echo Press Ctrl+C to stop the server
echo.
python manage.py runserver

