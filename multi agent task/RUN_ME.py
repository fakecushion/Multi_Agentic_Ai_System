#!/usr/bin/env python3
"""
RUN_ME.py - Quick start script for the Multi-Agent AI System

This script provides a simple way to get started with the multi-agent system.
"""

import os
import sys
import subprocess
import webbrowser
import time

def main():
    print("=" * 60)
    print("Multi-Agent AI System - Quick Start")
    print("=" * 60)
    
    print("\nChecking system requirements...")
    
    # Check if Python is available
    try:
        python_version = sys.version.split()[0]
        print(f"✓ Python {python_version} available")
    except Exception as e:
        print(f"✗ Python not available: {e}")
        return
    
    # Check if required packages are installed
    required_packages = [
        "fastapi",
        "uvicorn",
        "fitz",  # PyMuPDF
        "faiss",
        "sentence_transformers"
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            if package == "fitz":
                import fitz
            elif package == "sentence_transformers":
                from sentence_transformers import SentenceTransformer
            else:
                __import__(package)
            print(f"✓ {package} installed")
        except ImportError:
            print(f"✗ {package} missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\nMissing packages: {', '.join(missing_packages)}")
        print("Please install them with: pip install -r requirements.txt")
        return
    
    print("\n" + "=" * 60)
    print("Starting the Multi-Agent AI System")
    print("=" * 60)
    
    # Start the server in the background
    print("Starting FastAPI server...")
    try:
        # Start the server
        server_process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", 
            "main:app", "--reload", "--host", "127.0.0.1", "--port", "8000"
        ])
        
        print("✓ Server started successfully")
        print("  URL: http://127.0.0.1:8000")
        
        # Wait a moment for the server to start
        time.sleep(3)
        
        # Open the frontend in a browser
        print("\nOpening frontend in browser...")
        frontend_path = os.path.abspath("frontend.html")
        webbrowser.open(f"file://{frontend_path}")
        
        print("✓ Frontend opened successfully")
        print("  File:", frontend_path)
        
        print("\n" + "=" * 60)
        print("System is now running!")
        print("=" * 60)
        print("Instructions:")
        print("1. Use the web interface to ask questions")
        print("2. Upload PDFs for RAG processing")
        print("3. View logs to see agent decisions")
        print("\nTo stop the system, press Ctrl+C in this terminal")
        
        # Keep the script running
        try:
            server_process.wait()
        except KeyboardInterrupt:
            print("\n\nShutting down...")
            server_process.terminate()
            server_process.wait()
            print("System stopped.")
            
    except Exception as e:
        print(f"Error starting system: {e}")
        return

if __name__ == "__main__":
    main()