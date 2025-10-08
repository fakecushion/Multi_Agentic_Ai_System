import os
import sys
from app.agents.pdf_rag import PDFRAGAgent

def initialize_system():
    """Initialize the system and process sample PDFs"""
    print("Initializing Multi-Agent AI System...")
    
    # Create necessary directories
    os.makedirs("uploads", exist_ok=True)
    os.makedirs("sample_pdfs", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    
    print("Directories created successfully!")
    
    # Initialize PDF RAG agent which will process sample PDFs
    print("Processing sample PDFs...")
    try:
        pdf_agent = PDFRAGAgent()
        print("PDF RAG agent initialized successfully!")
    except Exception as e:
        print(f"Error initializing PDF RAG agent: {e}")
    
    print("System initialization complete!")
    print("\nTo start the server, run:")
    print("uvicorn main:app --reload")
    print("\nTo access the frontend, open frontend.html in your browser")

if __name__ == "__main__":
    initialize_system()