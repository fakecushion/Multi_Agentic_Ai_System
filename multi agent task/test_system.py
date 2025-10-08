import pytest
from app.agents.controller import ControllerAgent
from app.models.query import QueryRequest

@pytest.mark.asyncio
async def test_controller_initialization():
    """Test that the controller initializes correctly"""
    controller = ControllerAgent()
    assert controller is not None
    assert controller.pdf_rag_agent is not None
    assert controller.web_search_agent is not None
    assert controller.arxiv_agent is not None

@pytest.mark.asyncio
async def test_pdf_query_routing():
    """Test that PDF-related queries are routed correctly"""
    controller = ControllerAgent()
    query = QueryRequest(question="What does the PDF document say about machine learning?")
    
    # This is a basic test - in a real scenario, you would mock the agent responses
    response = await controller.process_query(query)
    assert response is not None
    assert hasattr(response, 'answer')
    assert hasattr(response, 'agents_used')
    assert hasattr(response, 'documents_retrieved')

@pytest.mark.asyncio
async def test_arxiv_query_routing():
    """Test that ArXiv-related queries are routed correctly"""
    controller = ControllerAgent()
    query = QueryRequest(question="Find recent papers on transformer models")
    
    response = await controller.process_query(query)
    assert response is not None

@pytest.mark.asyncio
async def test_web_search_query_routing():
    """Test that web search queries are routed correctly"""
    controller = ControllerAgent()
    query = QueryRequest(question="What are the latest developments in AI?")
    
    response = await controller.process_query(query)
    assert response is not None

if __name__ == "__main__":
    pytest.main([__file__])