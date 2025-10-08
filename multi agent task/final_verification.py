"""
Final verification script to check all components
"""
import sys
import os

def verify_components():
    """Verify all system components"""
    print("=== Multi-Agent System Verification ===\n")
    
    # Check Python version
    print(f"Python version: {sys.version}")
    
    # Check current directory
    print(f"Current directory: {os.getcwd()}")
    
    # Check if required files exist
    required_files = [
        "main.py",
        "requirements.txt",
        "frontend.html",
        "README.md",
        "REPORT.pdf",
        "Dockerfile",
        "app/api/routes.py",
        "app/agents/controller.py",
        "app/agents/pdf_rag.py",
        "app/agents/web_search.py",
        "app/agents/arxiv.py"
    ]
    
    print("\nChecking required files:")
    for file in required_files:
        if os.path.exists(file):
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file}")
    
    # Check sample PDFs
    print("\nChecking sample PDFs:")
    sample_pdfs_dir = "sample_pdfs"
    if os.path.exists(sample_pdfs_dir):
        pdf_files = os.listdir(sample_pdfs_dir)
        for pdf in pdf_files:
            if pdf.endswith(".pdf"):
                print(f"  ✓ {pdf}")
    else:
        print("  ✗ sample_pdfs directory not found")
    
    # Test imports
    print("\nTesting imports:")
    try:
        from fastapi import FastAPI
        print("  ✓ FastAPI")
    except ImportError as e:
        print(f"  ✗ FastAPI: {e}")
    
    try:
        import fitz
        print("  ✓ PyMuPDF (fitz)")
    except ImportError as e:
        print(f"  ✗ PyMuPDF: {e}")
    
    try:
        import faiss
        print("  ✓ FAISS")
    except ImportError as e:
        print(f"  ✗ FAISS: {e}")
    
    try:
        from sentence_transformers import SentenceTransformer
        print("  ✓ Sentence Transformers")
    except ImportError as e:
        print(f"  ✗ Sentence Transformers: {e}")
    
    try:
        import arxiv
        print("  ✓ ArXiv")
    except ImportError as e:
        print(f"  ✗ ArXiv: {e}")
    
    try:
        from bs4 import BeautifulSoup
        print("  ✓ BeautifulSoup")
    except ImportError as e:
        print(f"  ✗ BeautifulSoup: {e}")
    
    try:
        from reportlab.platypus import SimpleDocTemplate
        print("  ✓ ReportLab")
    except ImportError as e:
        print(f"  ✗ ReportLab: {e}")
    
    print("\n=== Verification Complete ===")

if __name__ == "__main__":
    verify_components()