#!/usr/bin/env python3
"""
TerraNova Application Runner
This script sets up and runs both the backend and frontend servers
NO STREAMLIT - Pure HTML/CSS/JavaScript frontend
"""

import subprocess
import sys
import time
import webbrowser
import os
import signal
from threading import Thread

def install_requirements():
    """Install required Python packages"""
    print("📦 Installing Python dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def run_backend():
    """Run the FastAPI backend server"""
    print("🚀 Starting FastAPI backend server...")
    os.chdir("backend")
    try:
        subprocess.call([sys.executable, "-m", "uvicorn", "main:app", "--reload", "--host", "127.0.0.1", "--port", "8000"])
    except KeyboardInterrupt:
        print("\n🛑 Backend server stopped")
    finally:
        os.chdir("..")

def open_frontend():
    """Open the frontend in browser"""
    print("🌐 Opening TerraNova frontend...")
    time.sleep(3)  # Wait for backend to start
    
    # Try to open with local server first, fallback to file://
    frontend_urls = [
        "http://localhost:3000",  # If serve_frontend.py is running
        f"file:///{os.path.abspath('frontend/index.html')}"  # Direct file access
    ]
    
    for url in frontend_urls:
        try:
            webbrowser.open(url)
            print(f"📱 Frontend opened at: {url}")
            break
        except Exception as e:
            print(f"⚠️ Could not open {url}: {e}")
            continue

def run_frontend_server():
    """Run a simple HTTP server for the frontend"""
    print("🌐 Starting frontend HTTP server...")
    time.sleep(2)  # Wait for backend to start
    try:
        subprocess.call([sys.executable, "serve_frontend.py"])
    except KeyboardInterrupt:
        print("\n🛑 Frontend server stopped")

def main():
    """Main function to coordinate the application startup"""
    print("🏙️ TerraNova - AI Future City Builder")
    print("🚀 Pure HTML/CSS/JavaScript Frontend")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("backend") or not os.path.exists("frontend"):
        print("❌ Error: Please run this script from the TerraNova root directory")
        return
    
    # Install dependencies
    if not install_requirements():
        return
    
    print("\n🎯 Starting TerraNova Application...")
    print("📍 Backend API: http://127.0.0.1:8000")
    print("📍 Frontend: http://localhost:3000 (or file:// fallback)")
    print("📍 Landing Page: file://index.html")
    print("\n⚠️  Keep this terminal open while using the application")
    print("⚠️  Press Ctrl+C to stop all servers\n")
    
    try:
        # Start backend in a separate thread
        backend_thread = Thread(target=run_backend, daemon=True)
        backend_thread.start()
        
        # Start frontend server in a separate thread
        frontend_thread = Thread(target=run_frontend_server, daemon=True)
        frontend_thread.start()
        
        # Open browser
        open_frontend()
        
        # Keep main thread alive
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Shutting down TerraNova...")
        print("👋 Thank you for using TerraNova!")

if __name__ == "__main__":
    main()
