#!/usr/bin/env python3
"""
Start script for the Multi-Agent AI System
This script starts both the backend API and serves the frontend
"""

import subprocess
import sys
import os
import threading
import time
import webbrowser

def start_backend():
    """Start the FastAPI backend"""
    print("Starting FastAPI backend...")
    try:
        # Start the FastAPI server
        backend_process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", 
            "main:app", "--host", "127.0.0.1", "--port", "8000"
        ])
        print("✓ FastAPI backend started on http://127.0.0.1:8000")
        return backend_process
    except Exception as e:
        print(f"✗ Failed to start backend: {e}")
        return None

def start_frontend():
    """Start the frontend server"""
    print("Starting frontend server...")
    try:
        # Start a simple HTTP server for the frontend
        frontend_process = subprocess.Popen([
            sys.executable, "-m", "http.server", "8080"
        ])
        print("✓ Frontend server started on http://localhost:8080")
        return frontend_process
    except Exception as e:
        print(f"✗ Failed to start frontend server: {e}")
        return None

def main():
    print("=" * 60)
    print("Multi-Agent AI System - Startup Script")
    print("=" * 60)
    
    # Start backend
    backend_process = start_backend()
    if not backend_process:
        return
    
    # Wait a moment for backend to start
    time.sleep(3)
    
    # Start frontend
    frontend_process = start_frontend()
    if not frontend_process:
        backend_process.terminate()
        return
    
    # Wait a moment for frontend to start
    time.sleep(2)
    
    # Open browser
    print("\nOpening browser...")
    try:
        webbrowser.open("http://localhost:8080/frontend.html")
        print("✓ Browser opened to frontend interface")
    except Exception as e:
        print(f"⚠ Could not open browser automatically: {e}")
        print("  Please manually navigate to http://localhost:8080/frontend.html")
    
    print("\n" + "=" * 60)
    print("System is now running!")
    print("=" * 60)
    print("Backend API:  http://127.0.0.1:8000")
    print("Frontend UI:  http://localhost:8080/frontend.html")
    print("\nPress Ctrl+C to stop both servers")
    print("=" * 60)
    
    try:
        # Wait for both processes
        backend_process.wait()
        frontend_process.wait()
    except KeyboardInterrupt:
        print("\n\nShutting down servers...")
        backend_process.terminate()
        frontend_process.terminate()
        
        # Wait for processes to terminate
        try:
            backend_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            backend_process.kill()
            
        try:
            frontend_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            frontend_process.kill()
            
        print("Servers stopped.")

if __name__ == "__main__":
    main()