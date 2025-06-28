@echo off
echo Starting TailorTalk Full Application...
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

echo Starting both backend and frontend...
echo Backend will run on http://localhost:8000
echo Frontend will run on http://localhost:8501
echo.

REM Start backend in a new window
start "TailorTalk Backend" cmd /k "call tailortalk-env\Scripts\activate.bat && set API_URL=http://localhost:8000/api/chat && uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload"

REM Wait a moment for backend to start
timeout /t 3 /nobreak > nul

REM Start frontend in a new window
start "TailorTalk Frontend" cmd /k "call tailortalk-env\Scripts\activate.bat && set API_URL=http://localhost:8000/api/chat && streamlit run frontend/app.py --server.port 8501"

echo Both applications are starting...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:8501
echo.
echo Press any key to close this window (applications will continue running)
pause > nul 