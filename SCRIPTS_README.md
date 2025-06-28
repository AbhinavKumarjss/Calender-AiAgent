# TailorTalk - Command Scripts Guide

This guide explains how to use the command scripts to run your TailorTalk project.

## 📁 Available Scripts

### Windows (.bat files)
- `run_backend.bat` - Start backend server only
- `run_frontend.bat` - Start frontend app only  
- `run_full_app.bat` - Start both backend and frontend

### Unix/Linux/Mac (.sh files)
- `run_backend.sh` - Start backend server only
- `run_frontend.sh` - Start frontend app only
- `run_full_app.sh` - Start both backend and frontend
- `setup.sh` - Initial setup script

## 🚀 Quick Start

### For Windows Users:
1. **First time setup:**
   ```cmd
   run_backend.bat
   ```
   This will create virtual environment and install dependencies.

2. **Run the full application:**
   ```cmd
   run_full_app.bat
   ```
   This opens both backend and frontend in separate windows.

### For Unix/Linux/Mac Users:
1. **First time setup:**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

2. **Run the full application:**
   ```bash
   ./run_full_app.sh
   ```

## 📋 Individual Scripts

### Backend Only
- **Windows:** `run_backend.bat`
- **Unix:** `./run_backend.sh`
- **URL:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

### Frontend Only
- **Windows:** `run_frontend.bat`
- **Unix:** `./run_frontend.sh`
- **URL:** http://localhost:8501
- **Note:** Backend must be running first!

### Both Applications
- **Windows:** `run_full_app.bat`
- **Unix:** `./run_full_app.sh`
- **Backend:** http://localhost:8000
- **Frontend:** http://localhost:8501

## ⚙️ What Each Script Does

1. **Checks for virtual environment** - Creates one if it doesn't exist
2. **Activates virtual environment** - Ensures proper Python environment
3. **Installs dependencies** - Updates packages from requirements.txt
4. **Sets environment variables** - Configures API_URL
5. **Starts the application(s)** - Runs the appropriate servers

## 🔧 Environment Variables

The scripts automatically set:
- `API_URL=http://localhost:8000/api/chat`

Make sure you have your `.env` file in the `backend/` directory with:
- `GOOGLE_CLIENT_ID`
- `GOOGLE_CLIENT_SECRET`
- `GEMINI_API_KEY`

## 🛠️ Troubleshooting

### Common Issues:

1. **Port already in use:**
   - Stop any existing servers
   - Check if ports 8000 or 8501 are free

2. **Virtual environment issues:**
   - Delete `tailortalk-env` folder
   - Run setup script again

3. **Dependencies not found:**
   - Run `pip install -r requirements.txt` manually
   - Check Python version (3.7+ required)

4. **Permission denied (Unix):**
   - Run `chmod +x *.sh` to make scripts executable

### Manual Commands:
```bash
# Create virtual environment
python -m venv tailortalk-env

# Activate (Windows)
tailortalk-env\Scripts\activate

# Activate (Unix)
source tailortalk-env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run backend
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload

# Run frontend
streamlit run frontend/app.py --server.port 8501
```

## 📱 Accessing Your Application

- **Frontend:** Open http://localhost:8501 in your browser
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs
- **Interactive API:** http://localhost:8000/redoc

## 🛑 Stopping Applications

- **Windows:** Close the command windows or press Ctrl+C
- **Unix:** Press Ctrl+C in the terminal
- **Full app script:** Press Ctrl+C to stop both applications

## 🔄 Development Workflow

1. **Start development:** `run_full_app.sh` or `run_full_app.bat`
2. **Make changes** to your code
3. **Auto-reload** - Both servers will automatically reload on file changes
4. **Stop:** Ctrl+C when done

Happy coding! 🎉 