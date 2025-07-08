@echo off
echo.
echo 🌍 African Companies Chat Assistant
echo ===================================
echo.

REM Check if virtual environment exists
if not exist ".venv\Scripts\python.exe" (
    echo ❌ Virtual environment not found!
    echo Please create a virtual environment first:
    echo    python -m venv .venv
    echo    .venv\Scripts\activate
    echo    pip install -r requirements.txt
    pause
    exit /b 1
)

REM Check if .env file exists
if not exist ".env" (
    echo ⚠️  Warning: .env file not found!
    echo Please copy .env.example to .env and add your OpenAI API key.
    echo.
)

echo 🚀 Starting server...
echo 📍 Server will be available at: http://localhost:8000
echo 🔧 Debug interface: http://localhost:8000/debug
echo 📊 API documentation: http://localhost:8000/docs
echo ⏹️  Press Ctrl+C to stop the server
echo.

REM Change to backend directory and start server
cd backend
"..\\.venv\\Scripts\\python.exe" -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

echo.
echo 👋 Server stopped
pause
