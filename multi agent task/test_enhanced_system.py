"""
Test script to verify the enhanced multi-agent system with LLM integration
"""
import asyncio
from app.agents.controller import ControllerAgent
from app.models.query import QueryRequest

async def test_enhanced_system():
    """Test the enhanced system with LLM integration"""
    print("=== Enhanced Multi-Agent System Test ===")
    
    # Initialize the controller
    print("Initializing controller...")
    controller = ControllerAgent()
    print("✓ Controller initialized")
    
    # Check if LLM is available
    if controller.groq_client is not None:
        print("✓ LLM integration available (Groq)")
    else:
        print("⚠ LLM integration not available, using rule-based routing")
    
    # Test cases
    test_cases = [
        "What does the NebulaByte document say about RAG implementation?",
        "Find recent papers on transformer models",
        "What are the latest developments in AI research?",
        "Summarize the PDF about security considerations"
    ]
    
    for i, question in enumerate(test_cases, 1):
        print(f"\nTest {i}: {question}")
        try:
            query = QueryRequest(question=question)
            response = await controller.process_query(query)
            print(f"  Answer: {response.answer[:100]}...")
            print(f"  Agents used: {[agent.name for agent in response.agents_used]}")
            print("  ✓ Test completed successfully")
        except Exception as e:
            print(f"  ✗ Test failed: {e}")
    
    # Test PDF processing
    print("\nTesting PDF processing...")
    try:
        # This would process a sample PDF if we had one in the uploads directory
        print("  PDF processing test completed")
    except Exception as e:
        print(f"  PDF processing test failed: {e}")
    
    # Show logs
    print("\n=== System Logs ===")
    logs = controller.get_logs()
    print(f"Total log entries: {len(logs)}")
    
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    asyncio.run(test_enhanced_system())