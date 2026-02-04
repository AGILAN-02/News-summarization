#!/bin/bash
# News Article Summarizer - Quick Start Script (macOS/Linux)
# This script sets up and runs the Streamlit app

echo ""
echo "========================================"
echo "    News Article Summarizer Setup"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8+ from https://www.python.org"
    exit 1
fi

echo "[1/4] Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create virtual environment"
    exit 1
fi

echo "[2/4] Activating virtual environment..."
source venv/bin/activate

echo "[3/4] Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

echo "[4/4] Starting Streamlit app..."
echo ""
echo "========================================"
echo "    Opening app at http://localhost:8501"
echo "========================================"
echo ""

streamlit run app.py
