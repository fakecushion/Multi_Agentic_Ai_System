def verify_installation():
    """Verify that all required packages are installed"""
    required_packages = [
        "fastapi",
        "uvicorn",
        "pydantic",
        "faiss",
        "fitz",  # PyMuPDF
        "sentence_transformers",
        "arxiv",
        "requests",
        "beautifulsoup4",
        "reportlab"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == "faiss":
                import faiss
            elif package == "fitz":
                import fitz
            elif package == "sentence_transformers":
                from sentence_transformers import SentenceTransformer
            else:
                __import__(package)
            print(f"✓ {package} is installed")
        except ImportError:
            print(f"✗ {package} is missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\nMissing packages: {', '.join(missing_packages)}")
        print("Please install them with: pip install -r requirements.txt")
        return False
    else:
        print("\n✓ All required packages are installed!")
        return True

if __name__ == "__main__":
    verify_installation()