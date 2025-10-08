from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os

def create_pdf(content, filename):
    """Create a PDF file with the given content"""
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Split content into paragraphs
    paragraphs = content.split('\n\n')
    
    for para in paragraphs:
        if para.strip():
            p = Paragraph(para, styles["Normal"])
            story.append(p)
            story.append(Spacer(1, 12))
    
    doc.build(story)

def generate_sample_pdfs():
    """Generate sample PDFs for the RAG demo"""
    # Sample NebulaByte dialog content
    pdf_contents = [
        {
            "filename": "nebulabyte_dialog_1.pdf",
            "content": """NebulaByte AI Consultation - Technical Architecture Discussion

Date: October 5, 2025

Participants: Dr. Sarah Chen (Lead AI Architect), Michael Rodriguez (Software Engineer), Lisa Wong (Product Manager)

Discussion Summary:

The team discussed the technical architecture for the new multi-agent system. The proposed solution involves four core agents: Controller, PDF RAG, Web Search, and ArXiv agents. The Controller agent will use a combination of rule-based logic and LLM-based decision making to route queries to the appropriate agents.

Technical Requirements:
1. FastAPI backend for API endpoints
2. FAISS vector store for PDF document retrieval
3. Integration with Groq API for LLM processing
4. Secure PDF upload with size limitations
5. Comprehensive logging of all agent interactions

Next Steps:
- Implement Controller agent decision logic
- Set up FAISS vector store for RAG
- Integrate with web search APIs
- Create basic frontend interface
"""
        },
        {
            "filename": "nebulabyte_dialog_2.pdf",
            "content": """NebulaByte AI Consultation - RAG Implementation Details

Date: October 6, 2025

Participants: Dr. Sarah Chen (Lead AI Architect), James Wilson (ML Engineer), Lisa Wong (Product Manager)

Retrieval-Augmented Generation (RAG) Implementation Plan:

The PDF RAG agent will be responsible for processing uploaded documents and enabling semantic search capabilities. The implementation will use the following components:

1. Text Extraction:
   - PyMuPDF (fitz) for PDF text extraction
   - Support for various PDF formats and layouts

2. Text Chunking:
   - Chunk size: 500 tokens with 50 token overlap
   - Semantic chunking to preserve context

3. Embedding Model:
   - SentenceTransformer 'all-MiniLM-L6-v2' for efficient encoding
   - 384-dimensional embeddings

4. Vector Store:
   - FAISS for fast similarity search
   - Index persistence for session continuity

5. Retrieval:
   - Top-K nearest neighbor search
   - Re-ranking based on relevance scores

Performance Targets:
- Document processing: < 5 seconds for 10-page PDF
- Search response: < 1 second
- Accuracy: > 85% relevant results
"""
        },
        {
            "filename": "nebulabyte_dialog_3.pdf",
            "content": """NebulaByte AI Consultation - Web Search and ArXiv Integration

Date: October 7, 2025

Participants: Dr. Sarah Chen (Lead AI Architect), Emma Thompson (Data Scientist), Michael Rodriguez (Software Engineer)

Web Search Agent Implementation:

The Web Search agent will provide real-time information retrieval capabilities. The implementation plan includes:

1. API Integration:
   - Primary: SerpAPI for comprehensive search results
   - Fallback: DuckDuckGo Instant Answer API
   - Rate limiting handling with exponential backoff

2. Result Processing:
   - Snippet extraction and summarization
   - Source credibility assessment
   - Duplicate result filtering

ArXiv Agent Implementation:

The ArXiv agent will focus on academic paper retrieval:

1. Data Sources:
   - ArXiv API for recent papers
   - Hugging Face datasets as backup

2. Paper Processing:
   - Title and abstract extraction
   - Author and publication date parsing
   - Category classification

3. Response Formatting:
   - Concise paper summaries
   - Direct links to full papers
   - Citation information
"""
        },
        {
            "filename": "nebulabyte_dialog_4.pdf",
            "content": """NebulaByte AI Consultation - Controller Agent Decision Logic

Date: October 8, 2025

Participants: Dr. Sarah Chen (Lead AI Architect), James Wilson (ML Engineer), Emma Thompson (Data Scientist)

Controller Agent Decision Logic Specification:

The Controller agent is the central orchestrator that determines which agents to engage for each query. The decision logic follows a two-tiered approach:

Rule-Based Routing (Primary):
1. PDF/Document Queries:
   - Keywords: "pdf", "document", "file", "upload"
   - Action: Route to PDF RAG agent

2. Academic Paper Queries:
   - Keywords: "paper", "research", "study", "arxiv", "recent papers"
   - Action: Route to ArXiv agent

3. Current Events Queries:
   - Keywords: "latest news", "recent developments", "current events", "today"
   - Action: Route to Web Search agent

4. Default:
   - All other queries route to Web Search agent

LLM-Based Enhancement (Secondary):
- For complex queries, use Groq API to refine routing decisions
- Context-aware agent selection based on query intent
- Dynamic combination of multiple agents when appropriate

Logging Requirements:
- Input query
- Routing decision with rationale
- Agents called
- Documents retrieved
- Final synthesized response
"""
        },
        {
            "filename": "nebulabyte_dialog_5.pdf",
            "content": """NebulaByte AI Consultation - Deployment and Security Considerations

Date: October 9, 2025

Participants: Dr. Sarah Chen (Lead AI Architect), Michael Rodriguez (Software Engineer), Lisa Wong (Product Manager)

Deployment Strategy:

The multi-agent system will be deployed using containerized microservices:

1. Backend Services:
   - FastAPI application container
   - FAISS vector store persistence
   - Redis for caching and session management

2. Frontend:
   - Static HTML/CSS/JS served via CDN
   - WebSocket connection for real-time updates

3. Hosting Platforms:
   - Primary: Hugging Face Spaces
   - Backup: Render.com
   - Local development: Docker Compose

Security Measures:

1. API Security:
   - Rate limiting per IP and user
   - API key authentication for external services
   - Input validation and sanitization

2. File Upload Security:
   - Maximum file size: 10MB
   - File type validation (PDF only)
   - Content scanning for malicious code
   - Temporary storage with automatic cleanup

3. Data Privacy:
   - No PII storage in logs
   - Encrypted data transmission (HTTPS)
   - GDPR-compliant data handling

Monitoring and Logging:
- Real-time system health monitoring
- Performance metrics collection
- Error tracking and alerting
- Audit logs for compliance
"""
        }
    ]
    
    # Create the PDFs
    for pdf_info in pdf_contents:
        filepath = os.path.join("sample_pdfs", pdf_info["filename"])
        create_pdf(pdf_info["content"], filepath)
        print(f"Created {filepath}")

if __name__ == "__main__":
    generate_sample_pdfs()