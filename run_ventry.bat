@echo off
chcp 65001 >nul
:: Ventry Inventory Manager Launcher for Windows
:: This batch file launches the Ventry application

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                                                              ║
echo ║   ██╗   ██╗███████╗███╗   ██╗████████╗██████╗ ██╗   ██╗    ║
echo ║   ██║   ██║██╔════╝████╗  ██║╚══██╔══╝██╔══██╗╚██╗ ██╔╝    ║
echo ║   ██║   ██║█████╗  ██╔██╗ ██║   ██║   ██████╔╝ ╚████╔╝     ║
echo ║   ╚██╗ ██╔╝██╔══╝  ██║╚██╗██║   ██║   ██╔══██╗  ╚██╔╝      ║
echo ║    ╚████╔╝ ███████╗██║ ╚████║   ██║   ██║  ██║   ██║       ║
echo ║     ╚═══╝  ╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝   ╚═╝       ║
echo ║                                                              ║
echo ║           Inventory Manager - Quick Start Guide              ║
echo ║                                                              ║
echo ║   Developer : github.com/githubsantu                          ║
echo ║   Website   : https://imdevops.in                              ║
echo ║                                                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo Starting application...
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

:: Check if PyQt5 is installed
python -c "import PyQt5" >nul 2>&1
if errorlevel 1 (
    echo PyQt5 not found. Installing...
    pip install PyQt5
)

:: Run the application
python main.py

pause
