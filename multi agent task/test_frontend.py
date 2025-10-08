"""
Test script to verify the frontend can be served correctly
"""

import os
import sys
import subprocess
import time
import requests

def test_frontend_serving():
    """Test that the frontend can be served correctly"""
    print("=== Frontend Serving Test ===")
    
    # Check if frontend.html exists
    if os.path.exists("frontend.html"):
        print("✓ frontend.html found")
    else:
        print("✗ frontend.html not found")
        return
    
    # Try to start a simple HTTP server
    print("Starting HTTP server for frontend...")
    try:
        # Start server in background
        server_process = subprocess.Popen([
            sys.executable, "-m", "http.server", "8081"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Wait for server to start
        time.sleep(2)
        
        # Try to access the frontend
        try:
            response = requests.get("http://localhost:8081/frontend.html", timeout=5)
            if response.status_code == 200:
                print("✓ Frontend served successfully")
                print(f"  Content length: {len(response.text)} characters")
                # Check if it contains expected elements
                if "<title>Multi-Agent AI System</title>" in response.text:
                    print("✓ Frontend title found")
                else:
                    print("⚠ Frontend title not found")
            else:
                print(f"✗ Failed to serve frontend: HTTP {response.status_code}")
        except requests.RequestException as e:
            print(f"✗ Failed to access frontend: {e}")
        
        # Stop the server
        server_process.terminate()
        try:
            server_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server_process.kill()
            
        print("HTTP server stopped.")
        
    except Exception as e:
        print(f"✗ Failed to start HTTP server: {e}")
    
    print("=== Frontend Test Complete ===")

if __name__ == "__main__":
    test_frontend_serving()