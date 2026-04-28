@echo off
cd /d "%~dp0.."

echo === Document Q^&A Assistant Setup ===

REM Create .env from .env.example if it doesn't exist
if not exist ".env" (
    copy ".env.example" ".env"
    echo [INFO] .env file created from .env.example - fill in your API keys before running.
    pause
    exit /b 0
)

REM Create virtual environment if it doesn't exist
if not exist ".venv" (
    echo [INFO] Creating virtual environment...
    python -m venv .venv
)

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Install dependencies
echo [INFO] Installing dependencies...
pip install -r requirements.txt --quiet

REM Create data directories
if not exist "data\raw" mkdir data\raw
if not exist "data\vectordb" mkdir data\vectordb

echo [INFO] Setup complete. Starting Streamlit...
echo [INFO] Open http://localhost:8501 in your browser.
echo.

streamlit run frontend/streamlit_app.py
