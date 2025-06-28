@echo off
echo Starting TailorTalk Frontend...
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

REM Start the Streamlit frontend
echo Starting Streamlit app on http://localhost:8501
echo Make sure the backend server is running first!
echo Press Ctrl+C to stop the app
echo.
streamlit run frontend/app.py --server.port 8501

pause 