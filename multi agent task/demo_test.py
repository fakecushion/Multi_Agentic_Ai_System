"""
Demo script to test the multi-agent system functionality
"""
import asyncio
import os
from app.agents.controller import ControllerAgent
from app.models.query import QueryRequest

async def demo_test():
    """Run a demo test of the multi-agent system"""
    print("=== Multi-Agent AI System Demo ===\n")
    
    # Initialize the controller
    print("Initializing controller...")
    controller = ControllerAgent()
    print("✓ Controller initialized\n")
    
    # Test 1: Web search query
    print("Test 1: Web search query")
    web_query = QueryRequest(question="What are the latest developments in AI?")
    print(f"Query: {web_query.question}")
    web_response = await controller.process_query(web_query)
    print(f"Answer: {web_response.answer}")
    print(f"Agents used: {[agent.name for agent in web_response.agents_used]}")
    print("✓ Web search test completed\n")
    
    # Test 2: ArXiv query
    print("Test 2: ArXiv query")
    arxiv_query = QueryRequest(question="Find recent papers on transformer models")
    print(f"Query: {arxiv_query.question}")
    arxiv_response = await controller.process_query(arxiv_query)
    print(f"Answer: {arxiv_response.answer}")
    print(f"Agents used: {[agent.name for agent in arxiv_response.agents_used]}")
    print("✓ ArXiv search test completed\n")
    
    # Test 3: PDF query (if sample PDFs exist)
    print("Test 3: PDF query")
    pdf_query = QueryRequest(question="What does the NebulaByte document say about RAG implementation?")
    print(f"Query: {pdf_query.question}")
    pdf_response = await controller.process_query(pdf_query)
    print(f"Answer: {pdf_response.answer}")
    print(f"Agents used: {[agent.name for agent in pdf_response.agents_used]}")
    print("✓ PDF search test completed\n")
    
    # Show logs
    print("=== System Logs ===")
    logs = controller.get_logs()
    print(f"Total logs: {len(logs)}")
    for i, log in enumerate(logs[-3:]):  # Show last 3 logs
        print(f"Log {i+1}: {log.input} -> {log.final_answer[:50]}...")
    
    print("\n=== Demo Completed Successfully ===")

if __name__ == "__main__":
    asyncio.run(demo_test())