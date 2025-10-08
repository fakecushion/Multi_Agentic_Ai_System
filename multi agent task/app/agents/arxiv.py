import arxiv
from typing import List, Dict

class ArxivAgent:
    def __init__(self):
        self.client = arxiv.Client()
    
    def search(self, query: str, max_results: int = 5) -> dict:
        """Search ArXiv for papers related to the query"""
        try:
            # Search for papers
            search = arxiv.Search(
                query=query,
                max_results=max_results,
                sort_by=arxiv.SortCriterion.Relevance
            )
            
            results = []
            papers = list(self.client.results(search))
            
            for paper in papers:
                results.append({
                    "title": paper.title,
                    "content": paper.summary,
                    "url": paper.entry_id,
                    "authors": [author.name for author in paper.authors],
                    "published": paper.published.strftime("%Y-%m-%d") if paper.published else ""
                })
            
            # Create summary from the most relevant papers
            summary = " ".join([f"{paper['title']}: {paper['content'][:150]}..." for paper in results[:2]])
            
            return {
                "papers": results,
                "summary": summary if summary else f"No ArXiv papers found for query: {query}"
            }
        except Exception as e:
            return {
                "papers": [],
                "summary": f"Error during ArXiv search: {str(e)}"
            }