@echo off
echo ========================================
echo AI Reel Generator - Windows Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.10+ from https://www.python.org/
    pause
    exit /b 1
)

echo [1/6] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

echo [2/6] Activating virtual environment...
call venv\Scripts\activate.bat

echo [3/6] Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo [4/6] Setting up environment file...
if not exist .env (
    copy env.example .env
    echo.
    echo IMPORTANT: Please edit .env file and add your OPENAI_API_KEY
    echo Opening .env file in notepad...
    timeout /t 2 >nul
    notepad .env
) else (
    echo .env file already exists, skipping...
)

echo [5/6] Running database migrations...
python manage.py migrate
if errorlevel 1 (
    echo ERROR: Failed to run migrations
    pause
    exit /b 1
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Make sure OPENAI_API_KEY is set in .env file
echo 2. (Optional) Create admin user: python manage.py createsuperuser
echo 3. Start server: python manage.py runserver
echo.
echo To start the server, run: start_server.bat
echo.
pause

