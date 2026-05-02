@echo off
REM DeskSorter Premium Launcher for Windows

echo.
echo ================================
echo   DeskSorter Premium v2.0
echo ================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH!
    echo Please install Python 3.7+ from https://www.python.org/
    echo.
    pause
    exit /b 1
)

echo Checking dependencies...
python -m pip list | findstr /i "pillow send2trash schedule" >nul
if errorlevel 1 (
    echo.
    echo Installing missing dependencies...
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo ERROR: Failed to install dependencies!
        echo Please run: pip install -r requirements.txt
        pause
        exit /b 1
    )
)

echo.
echo ✓ All dependencies installed!
echo Launching DeskSorter Premium...
echo.

python desksorter_premium.py

if errorlevel 1 (
    echo.
    echo ERROR: Failed to start DeskSorter!
    echo Check that all files are in the correct directory.
    pause
    exit /b 1
)
