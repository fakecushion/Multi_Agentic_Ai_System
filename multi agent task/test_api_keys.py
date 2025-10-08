"""
Test script to verify API keys are working correctly
"""
import os
from app.config.settings import settings

def test_api_keys():
    """Test that all API keys are loaded correctly"""
    print("=== API Key Verification ===")
    
    # Test Groq API Key
    groq_key = settings.GROQ_API_KEY
    if groq_key:
        print("✓ Groq API Key loaded")
        # Check if it looks like a real key (starts with gsk_)
        if groq_key.startswith("gsk_"):
            print("✓ Groq API Key format looks correct")
        else:
            print("⚠ Groq API Key format may be incorrect")
    else:
        print("✗ Groq API Key not found")
    
    # Test Google AI API Key
    google_key = settings.GOOGLE_AI_API_KEY
    if google_key:
        print("✓ Google AI API Key loaded")
        # Check if it looks like a real key (starts with AIza)
        if google_key.startswith("AIza"):
            print("✓ Google AI API Key format looks correct")
        else:
            print("⚠ Google AI API Key format may be incorrect")
    else:
        print("✗ Google AI API Key not found")
    
    # Test SerpAPI Key
    serpapi_key = settings.SERPAPI_API_KEY
    if serpapi_key:
        print("✓ SerpAPI Key loaded")
        # Check length (should be 64 characters)
        if len(serpapi_key) == 64:
            print("✓ SerpAPI Key length looks correct")
        else:
            print(f"⚠ SerpAPI Key length may be incorrect: {len(serpapi_key)} characters")
    else:
        print("✗ SerpAPI Key not found")
    
    print("=== Verification Complete ===")

if __name__ == "__main__":
    test_api_keys()