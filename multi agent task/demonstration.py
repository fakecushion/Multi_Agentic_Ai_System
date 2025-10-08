"""
Demonstration script for the Multi-Agent AI System
"""
import requests
import time
import json

def demonstrate_system():
    """Demonstrate the multi-agent AI system"""
    print("=" * 60)
    print("Multi-Agent AI System Demonstration")
    print("=" * 60)
    
    # API endpoints
    BASE_URL = "http://127.0.0.1:8000"
    
    # Test 1: General question (should use web search)
    print("\n1. Testing Web Search Agent:")
    print("-" * 30)
    question = "What are the latest developments in artificial intelligence?"
    print(f"Question: {question}")
    
    response = requests.post(f"{BASE_URL}/ask", json={"question": question})
    if response.status_code == 200:
        data = response.json()
        print(f"Answer: {data['answer'][:200]}...")
        print(f"Agents Used: {[agent['name'] for agent in data['agents_used']]}")
        print("✓ Web search agent working correctly")
    else:
        print(f"✗ Error: {response.status_code}")
    
    time.sleep(2)
    
    # Test 2: PDF-related question (should use PDF RAG)
    print("\n2. Testing PDF RAG Agent:")
    print("-" * 30)
    question = "What does the NebulaByte document say about security considerations?"
    print(f"Question: {question}")
    
    response = requests.post(f"{BASE_URL}/ask", json={"question": question})
    if response.status_code == 200:
        data = response.json()
        print(f"Answer: {data['answer'][:200]}...")
        print(f"Agents Used: {[agent['name'] for agent in data['agents_used']]}")
        print("✓ PDF RAG agent working correctly")
    else:
        print(f"✗ Error: {response.status_code}")
    
    time.sleep(2)
    
    # Test 3: Academic question (should use ArXiv)
    print("\n3. Testing ArXiv Agent:")
    print("-" * 30)
    question = "Find recent papers on transformer models"
    print(f"Question: {question}")
    
    response = requests.post(f"{BASE_URL}/ask", json={"question": question})
    if response.status_code == 200:
        data = response.json()
        print(f"Answer: {data['answer'][:200]}...")
        print(f"Agents Used: {[agent['name'] for agent in data['agents_used']]}")
        print("✓ ArXiv agent working correctly")
    else:
        print(f"✗ Error: {response.status_code}")
    
    time.sleep(2)
    
    # Test 4: Check logs
    print("\n4. Checking System Logs:")
    print("-" * 30)
    
    response = requests.get(f"{BASE_URL}/logs")
    if response.status_code == 200:
        data = response.json()
        print(f"Total log entries: {len(data['logs'])}")
        if data['logs']:
            latest_log = data['logs'][-1]
            print(f"Latest query: {latest_log['input']}")
            print(f"Agents called: {latest_log['agents_called']}")
            print("✓ Logging system working correctly")
        else:
            print("No logs found")
    else:
        print(f"✗ Error: {response.status_code}")
    
    print("\n" + "=" * 60)
    print("Demonstration Complete!")
    print("The system is running and accessible at:")
    print("Frontend: http://localhost:8080/frontend.html")
    print("Backend API: http://127.0.0.1:8000")
    print("=" * 60)

if __name__ == "__main__":
    demonstrate_system()