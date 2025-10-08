"""
Startup script for Gradio interface
"""
import subprocess
import sys
import time
import os

def start_system():
    """Start both the backend API and Gradio interface"""
    print("=" * 60)
    print("Multi-Agent AI System with Gradio Interface")
    print("=" * 60)
    
    # Start the FastAPI backend in the background
    print("Starting FastAPI backend...")
    backend_process = subprocess.Popen([
        sys.executable, "-m", "uvicorn", 
        "main:app", "--host", "127.0.0.1", "--port", "8000"
    ])
    print("✓ FastAPI backend started on http://127.0.0.1:8000")
    
    # Wait a moment for backend to start
    print("Waiting for backend to initialize...")
    time.sleep(5)
    
    # Start the Gradio interface
    print("Starting Gradio interface...")
    try:
        from app.app import demo
        
        print("✓ Gradio interface started on http://localhost:7861")
        print("\n" + "=" * 60)
        print("System is now running!")
        print("=" * 60)
        print("Backend API:  http://127.0.0.1:8000")
        print("Gradio UI:    http://localhost:7861")
        print("\nPress Ctrl+C to stop both servers")
        print("=" * 60)
        
        # Launch Gradio with a different approach
        import threading
        def launch_gradio():
            demo.launch(server_name="0.0.0.0", server_port=7861, share=False, prevent_thread_lock=True)
        
        gradio_thread = threading.Thread(target=launch_gradio)
        gradio_thread.daemon = True
        gradio_thread.start()
        
        # Keep the script running
        try:
            backend_process.wait()
        except KeyboardInterrupt:
            print("\n\nShutting down servers...")
            backend_process.terminate()
            try:
                backend_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                backend_process.kill()
            print("Servers stopped.")
            
    except ImportError as e:
        print(f"✗ Error importing Gradio or demo: {e}")
        print("Please check that all required packages are installed")
        backend_process.terminate()
        return
    except Exception as e:
        print(f"✗ Error starting Gradio: {e}")
        backend_process.terminate()
        return

if __name__ == "__main__":
    start_system()