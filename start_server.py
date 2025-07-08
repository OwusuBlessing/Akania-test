#!/usr/bin/env python3
"""
Startup script for the African Companies Chat Assistant.
This script makes it easy to start the FastAPI server.
"""

import os
import sys
import subprocess
import argparse
import webbrowser
import time
from pathlib import Path

def main():
    """Start the FastAPI server for the African Companies Chat Assistant."""
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Start the African Companies Chat Assistant")
    parser.add_argument("--port", type=int, default=8000, help="Port to run the server on (default: 8000)")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind the server to (default: 0.0.0.0)")
    parser.add_argument("--no-reload", action="store_true", help="Disable auto-reload")
    parser.add_argument("--no-browser", action="store_true", help="Don't automatically open browser")
    args = parser.parse_args()
    
    # Get the project root directory
    project_root = Path(__file__).parent
    backend_dir = project_root / "backend"
    
    # Check if backend directory exists
    if not backend_dir.exists():
        print("❌ Error: backend directory not found!")
        print(f"Expected path: {backend_dir}")
        return 1
    
    # Check if main.py exists
    main_py = backend_dir / "main.py"
    if not main_py.exists():
        print("❌ Error: main.py not found in backend directory!")
        print(f"Expected path: {main_py}")
        return 1
    
    # Check if .env file exists
    env_file = project_root / ".env"
    if not env_file.exists():
        print("⚠️  Warning: .env file not found. Make sure you have your OpenAI API key configured.")
        print(f"Expected path: {env_file}")
        print("You can copy .env.example to .env and add your API key.")
    
    # Change to backend directory
    os.chdir(backend_dir)
    
    print("🚀 Starting African Companies Chat Assistant...")
    print(f"📍 Server will be available at: http://localhost:{args.port}")
    print(f"🔧 Debug interface: http://localhost:{args.port}/debug")
    print(f"📊 API documentation: http://localhost:{args.port}/docs")
    print("⏹️  Press Ctrl+C to stop the server")
    print("-" * 50)
    
    # Prepare uvicorn command
    cmd = [
        sys.executable, "-m", "uvicorn", 
        "main:app", 
        "--host", args.host, 
        "--port", str(args.port)
    ]
    
    if not args.no_reload:
        cmd.append("--reload")
    
    try:
        # Start the server using uvicorn
        if not args.no_browser:
            # Give server a moment to start, then open browser
            def open_browser():
                time.sleep(2)
                webbrowser.open(f"http://localhost:{args.port}")
            
            import threading
            browser_thread = threading.Thread(target=open_browser)
            browser_thread.daemon = True
            browser_thread.start()
        
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
        return 0
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting server: {e}")
        return 1
    except FileNotFoundError:
        print("❌ Error: uvicorn not found. Please install requirements:")
        print("pip install -r requirements.txt")
        return 1

if __name__ == "__main__":
    sys.exit(main())
