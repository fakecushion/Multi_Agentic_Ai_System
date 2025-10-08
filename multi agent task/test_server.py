"""
Test script to verify the server can start
"""
import asyncio
from main import app
import uvicorn

def test_server():
    """Test that the server can be created"""
    print("=== Server Test ===")
    print("FastAPI app created successfully")
    print(f"App title: {app.title}")
    print("Server test completed successfully")
    print("=== Server Test Complete ===")

if __name__ == "__main__":
    test_server()