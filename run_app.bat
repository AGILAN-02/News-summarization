@echo off
REM News Article Summarizer - Quick Start Script (Windows)
REM This script sets up and runs the Streamlit app

echo.
echo ========================================
echo    News Article Summarizer Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org
    pause
    exit /b 1
)

echo [1/4] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

echo [2/4] Activating virtual environment...
call venv\Scripts\activate.bat

echo [3/4] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo [4/4] Starting Streamlit app...
echo.
echo ========================================
echo    Opening app at http://localhost:8501
echo ========================================
echo.

streamlit run app.py

pause
