@echo off
echo Starting TailorTalk Backend Server...
echo.

REM Check if virtual environment exists
if not exist "tailortalk-env" (
    echo Creating virtual environment...
    python -m venv tailortalk-env
)

REM Activate virtual environment
echo Activating virtual environment...
call tailortalk-env\Scripts\activate.bat

REM Install/update dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Set environment variables
set API_URL=http://localhost:8000/api/chat

REM Start the backend server
echo Starting FastAPI server on http://localhost:8000
echo Press Ctrl+C to stop the server
echo.
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload

pause 