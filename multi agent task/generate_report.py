from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import io

def create_report():
    """Generate the REPORT.pdf document"""
    doc = SimpleDocTemplate("REPORT.pdf", pagesize=A4)
    styles = getSampleStyleSheet()
    story = []
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=1  # Center alignment
    )
    
    story.append(Paragraph("Multi-Agent AI System", title_style))
    story.append(Paragraph("Dynamic Decision Making Architecture", title_style))
    story.append(Spacer(1, 0.5*inch))
    
    # Authors
    story.append(Paragraph("Technical Implementation Report", styles['Heading2']))
    story.append(Spacer(1, 0.3*inch))
    
    # Table of Contents
    story.append(Paragraph("Table of Contents", styles['Heading2']))
    toc_items = [
        "1. Introduction",
        "2. System Architecture",
        "3. Agent Implementation",
        "4. Controller Decision Logic",
        "5. Security and Privacy",
        "6. Deployment",
        "7. Limitations and Future Work"
    ]
    
    for item in toc_items:
        story.append(Paragraph(item, styles['Normal']))
    
    story.append(Spacer(1, 0.3*inch))
    
    # 1. Introduction
    story.append(Paragraph("1. Introduction", styles['Heading2']))
    intro_text = """
    This report details the implementation of a multi-agent AI system with dynamic decision making capabilities. 
    The system is designed to intelligently route user queries to specialized agents based on the content and 
    context of the query. The architecture includes a controller agent that makes routing decisions, and 
    specialized agents for PDF document processing, web search, and academic paper retrieval.
    """
    story.append(Paragraph(intro_text, styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    
    # 2. System Architecture
    story.append(Paragraph("2. System Architecture", styles['Heading2']))
    arch_text = """
    The system follows a modular architecture with clearly defined components:
    """
    story.append(Paragraph(arch_text, styles['Normal']))
    
    # Architecture components as table
    arch_data = [
        ['Component', 'Description'],
        ['Controller Agent', 'Orchestrates the system and routes queries to appropriate agents'],
        ['PDF RAG Agent', 'Processes PDF documents and enables semantic search capabilities'],
        ['Web Search Agent', 'Performs real-time web searches for current information'],
        ['ArXiv Agent', 'Retrieves and summarizes recent academic papers'],
        ['Frontend', 'Provides user interface for queries and PDF uploads'],
        ['Backend API', 'FastAPI-based REST API serving all endpoints'],
        ['Logging System', 'Tracks all interactions and decisions for traceability']
    ]
    
    arch_table = Table(arch_data)
    arch_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(arch_table)
    story.append(Spacer(1, 0.2*inch))
    
    # 3. Agent Implementation
    story.append(Paragraph("3. Agent Implementation", styles['Heading2']))
    
    # PDF RAG Agent
    story.append(Paragraph("PDF RAG Agent", styles['Heading3']))
    pdf_text = """
    The PDF RAG (Retrieval-Augmented Generation) agent processes uploaded PDF documents using the following workflow:
    
    1. Text Extraction: Uses PyMuPDF (fitz) library to extract text from PDF files
    2. Text Chunking: Splits documents into 500-token chunks with 50-token overlap
    3. Embedding Generation: Uses SentenceTransformer 'all-MiniLM-L6-v2' to create 384-dimensional embeddings
    4. Vector Storage: Stores embeddings in FAISS vector store for efficient similarity search
    5. Retrieval: Performs nearest neighbor search to find relevant document chunks
    """
    story.append(Paragraph(pdf_text, styles['Normal']))
    story.append(Spacer(1, 0.1*inch))
    
    # Web Search Agent
    story.append(Paragraph("Web Search Agent", styles['Heading3']))
    web_text = """
    The Web Search agent provides real-time information retrieval using:
    
    1. DuckDuckGo Instant Answer API for primary search functionality
    2. Result parsing and filtering to extract relevant information
    3. Summarization of search results for concise responses
    """
    story.append(Paragraph(web_text, styles['Normal']))
    story.append(Spacer(1, 0.1*inch))
    
    # ArXiv Agent
    story.append(Paragraph("ArXiv Agent", styles['Heading3']))
    arxiv_text = """
    The ArXiv agent specializes in academic paper retrieval:
    
    1. Queries the official ArXiv API for recent papers
    2. Extracts paper metadata including titles, abstracts, and authors
    3. Provides concise summaries of relevant papers
    """
    story.append(Paragraph(arxiv_text, styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    
    # 4. Controller Decision Logic
    story.append(Paragraph("4. Controller Decision Logic", styles['Heading2']))
    controller_text = """
    The Controller agent uses a hybrid approach combining rule-based logic and LLM-based decision making:
    
    Rule-Based Routing:
    - Queries containing "pdf" or "document" → PDF RAG Agent
    - Queries containing "recent papers", "arxiv", or "paper" → ArXiv Agent
    - Queries containing "latest news" or "recent developments" → Web Search Agent
    - Default routing → Web Search Agent
    
    The controller logs all decisions including:
    - Input query
    - Routing decision with rationale
    - Agents called
    - Documents retrieved
    - Final synthesized response
    """
    story.append(Paragraph(controller_text, styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    
    # 5. Security and Privacy
    story.append(Paragraph("5. Security and Privacy", styles['Heading2']))
    security_text = """
    The system implements several security and privacy measures:
    
    1. File Upload Security:
       - Maximum file size limited to 10MB
       - File type validation (PDF only)
       - Temporary storage with automatic cleanup
    
    2. Data Privacy:
       - No PII storage in logs
       - Encrypted data transmission (HTTPS)
       - GDPR-compliant data handling
    
    3. API Security:
       - Rate limiting for all endpoints
       - Input validation and sanitization
    """
    story.append(Paragraph(security_text, styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    
    # 6. Deployment
    story.append(Paragraph("6. Deployment", styles['Heading2']))
    deployment_text = """
    The system is designed for deployment on Hugging Face Spaces:
    
    1. Containerization using Docker with the provided Dockerfile
    2. Environment variable configuration for API keys
    3. Automatic processing of sample PDFs on startup
    4. Health checks and monitoring capabilities
    """
    story.append(Paragraph(deployment_text, styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    
    # 7. Limitations and Future Work
    story.append(Paragraph("7. Limitations and Future Work", styles['Heading2']))
    limitations_text = """
    Current Limitations:
    - Rule-based routing could be enhanced with more sophisticated LLM-based decision making
    - PDF processing is limited to text extraction (no image or table processing)
    - Web search results depend on the quality of the search API
    
    Future Enhancements:
    - Integration with additional LLM APIs (Groq, Google AI Studio)
    - Advanced PDF processing including image and table extraction
    - User feedback mechanisms to improve routing decisions
    - Multi-language support
    """
    story.append(Paragraph(limitations_text, styles['Normal']))
    
    # Build PDF
    doc.build(story)
    print("REPORT.pdf generated successfully!")

if __name__ == "__main__":
    create_report()