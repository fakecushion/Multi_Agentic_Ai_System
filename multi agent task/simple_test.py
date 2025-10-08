"""
Simple test to verify the system components
"""
from app.agents.controller import ControllerAgent

def simple_test():
    """Simple test to verify system components"""
    print("Testing system components...")
    
    # Test controller initialization
    try:
        controller = ControllerAgent()
        print("✓ Controller initialized successfully")
        
        # Check LLM availability
        if controller.groq_client is not None:
            print("✓ LLM integration available")
        else:
            print("⚠ LLM integration not available")
            
    except Exception as e:
        print(f"✗ Controller initialization failed: {e}")
        return
    
    print("Simple test completed!")

if __name__ == "__main__":
    simple_test()