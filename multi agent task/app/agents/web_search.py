import requests
import os
from typing import List, Dict
from app.config.settings import settings

class WebSearchAgent:
    def __init__(self):
        self.api_key = settings.SERPAPI_API_KEY
        self.base_url = "https://serpapi.com/search"
    
    def search(self, query: str) -> dict:
        """Perform a web search using SerpAPI and return results"""
        try:
            # Use SerpAPI for web search
            params = {
                "q": query,
                "api_key": self.api_key,
                "engine": "google"
            }
            
            response = requests.get(self.base_url, params=params)
            data = response.json()
            
            # Extract relevant information
            results = []
            
            # Add organic search results
            if "organic_results" in data:
                for result in data["organic_results"][:5]:  # Limit to 5 results
                    results.append({
                        "title": result.get("title", ""),
                        "content": result.get("snippet", ""),
                        "url": result.get("link", "")
                    })
            
            # Create summary
            summary = " ".join([f"{result['title']}: {result['content'][:100]}..." for result in results[:2]])
            
            return {
                "results": results,
                "summary": summary if summary else f"No web results found for query: {query}"
            }
        except Exception as e:
            return {
                "results": [],
                "summary": f"Error during web search: {str(e)}"
            }