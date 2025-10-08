import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # API Keys
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    GOOGLE_AI_API_KEY = os.getenv("GOOGLE_AI_API_KEY", "")
    SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY", "")
    
    # File upload settings
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
    UPLOAD_DIR = "uploads"
    
    # RAG settings
    CHUNK_SIZE = 500
    CHUNK_OVERLAP = 50
    
    # ArXiv settings
    ARXIV_MAX_RESULTS = 5

settings = Settings()