"""


Quick test to verify the system components work
"""
import asyncio
from app.agents.controller import ControllerAgent
from app.models.query import QueryRequest

async def quick_test():
    """Run a quick test of the system components"""
    print("=== Quick System Test ===")
    
    # Test controller initialization
    try:
        controller = ControllerAgent()
        print("✓ Controller initialized successfully")
    except Exception as e:
        print(f"✗ Controller initialization failed: {e}")
        return
    
    # Test a simple query
    try:
        query = QueryRequest(question="What is the latest in AI research?")
        response = await controller.process_query(query)
        print("✓ Query processing successful")
        print(f"  Answer: {response.answer[:100]}...")
    except Exception as e:
        print(f"✗ Query processing failed: {e}")
    
    print("=== Test Complete ===")

if __name__ == "__main__":
    asyncio.run(quick_test())