import os
from typing import List, Tuple, Dict, Any, Optional
from app.models.query import QueryRequest, QueryResponse, AgentInfo, DocumentInfo
from app.models.log import LogEntry
from app.agents.pdf_rag import PDFRAGAgent
from app.agents.web_search import WebSearchAgent
from app.agents.arxiv import ArxivAgent
from app.config.settings import settings
import asyncio
from datetime import datetime
import json
import uuid

# Conditional import for Groq API
try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False
    Groq = None  # type: ignore
    print("Groq API not available. Using rule-based routing only.")

class ControllerAgent:
    def __init__(self):
        self.pdf_rag_agent = PDFRAGAgent()
        self.web_search_agent = WebSearchAgent()
        self.arxiv_agent = ArxivAgent()
        self.logs: List[LogEntry] = []
        self.log_file = "logs/system_logs.json"
        
        # Initialize Groq client if API key is available
        self.groq_client: Optional[Any] = None
        if GROQ_AVAILABLE and settings.GROQ_API_KEY and Groq is not None:
            try:
                self.groq_client = Groq(api_key=settings.GROQ_API_KEY)
            except Exception as e:
                print(f"Failed to initialize Groq client: {e}")
        
        self._load_logs()
        
    async def process_query(self, query: QueryRequest) -> QueryResponse:
        """Process a query by deciding which agents to use and synthesizing the response"""
        # Decision making logic
        agents_to_use, rationale = self._decide_agents(query.question)
        
        # Call the selected agents
        agent_responses = []
        documents_retrieved = []
        
        for agent_name in agents_to_use:
            if agent_name == "pdf_rag":
                response = self.pdf_rag_agent.search(query.question)
                agent_responses.append(("pdf_rag", response))
                documents_retrieved.extend(response.get("documents", []))
            elif agent_name == "web_search":
                response = self.web_search_agent.search(query.question)
                agent_responses.append(("web_search", response))
            elif agent_name == "arxiv":
                response = self.arxiv_agent.search(query.question)
                agent_responses.append(("arxiv", response))
                
        # Synthesize final answer
        final_answer = self._synthesize_response(query.question, agent_responses)
        
        # Create agent info for response
        agents_info = [
            AgentInfo(name=name, rationale=rationale.get(name, ""))
            for name in agents_to_use
        ]
        
        # Create document info for response
        docs_info = [
            DocumentInfo(id=doc.get("id", ""), title=doc.get("title", ""), content=doc.get("content", ""))
            for doc in documents_retrieved
        ]
        
        # Log the interaction
        log_entry = LogEntry(
            input=query.question,
            decision=str(rationale),
            agents_called=agents_to_use,
            documents_retrieved=[doc.get("id", "") for doc in documents_retrieved],
            final_answer=final_answer,
            timestamp=datetime.now()
        )
        self.logs.append(log_entry)
        self._save_logs()
        
        return QueryResponse(
            answer=final_answer,
            agents_used=agents_info,
            documents_retrieved=docs_info,
            timestamp=datetime.now()
        )
    
    async def process_pdf(self, file_path: str) -> dict:
        """Process an uploaded PDF file"""
        result = self.pdf_rag_agent.process_pdf(file_path)
        return result
    
    def _decide_agents(self, question: str) -> Tuple[List[str], Dict[str, str]]:
        """Decide which agents to use based on the question"""
        # If Groq is available, use it for enhanced decision making
        if self.groq_client is not None:
            try:
                return self._llm_decide_agents(question)
            except Exception as e:
                print(f"LLM decision making failed, falling back to rule-based: {e}")
        
        # Fallback to rule-based routing
        return self._rule_based_decide_agents(question)
    
    def _llm_decide_agents(self, question: str) -> Tuple[List[str], Dict[str, str]]:
        """Use LLM to decide which agents to use"""
        if self.groq_client is None:
            return self._rule_based_decide_agents(question)
            
        prompt = f"""
        Analyze the following question and determine which agents should be used to answer it.
        Available agents:
        1. pdf_rag: For questions about specific documents or PDF content
        2. web_search: For general questions, current events, or information that requires up-to-date data
        3. arxiv: For academic questions, research papers, or scientific topics
        
        Question: "{question}"
        
        Respond with a JSON object in this format:
        {{
            "agents": ["agent_name1", "agent_name2", ...],
            "rationale": "Explanation for why these agents were chosen"
        }}
        """
        
        try:
            chat_completion = self.groq_client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model="llama-3.1-70b-versatile",  # Updated model
                temperature=0.1,
                max_tokens=200,
            )
            
            response_text = chat_completion.choices[0].message.content
            if response_text is None:
                return self._rule_based_decide_agents(question)
                
            # Parse the JSON response (in a real implementation, you'd use proper JSON parsing)
            # For now, we'll fall back to rule-based if parsing fails
            response_text_lower = response_text.lower()
            if "pdf_rag" in response_text_lower or "document" in response_text_lower:
                agents = ["pdf_rag"]
                rationale = {"pdf_rag": "LLM determined PDF RAG agent is relevant"}
            elif "arxiv" in response_text_lower or "paper" in response_text_lower or "research" in response_text_lower:
                agents = ["arxiv"]
                rationale = {"arxiv": "LLM determined ArXiv agent is relevant"}
            else:
                agents = ["web_search"]
                rationale = {"web_search": "LLM determined Web Search agent is relevant"}
                
            return agents, rationale
        except Exception as e:
            print(f"Error in LLM decision making: {e}")
            # Fallback to rule-based
            return self._rule_based_decide_agents(question)
    
    def _rule_based_decide_agents(self, question: str) -> Tuple[List[str], Dict[str, str]]:
        """Rule-based agent decision making (fallback)"""
        agents_to_use = []
        rationale = {}
        
        # Rule-based routing
        if "pdf" in question.lower() or "document" in question.lower():
            agents_to_use.append("pdf_rag")
            rationale["pdf_rag"] = "Question relates to PDF/document content"
            
        if "recent papers" in question.lower() or "arxiv" in question.lower() or "paper" in question.lower() or "research" in question.lower():
            agents_to_use.append("arxiv")
            rationale["arxiv"] = "Question specifically asks for recent papers or arxiv content"
            
        if "latest news" in question.lower() or "recent developments" in question.lower() or "current events" in question.lower() or "today" in question.lower():
            agents_to_use.append("web_search")
            rationale["web_search"] = "Question asks for latest news or recent developments"
            
        # If no specific agents were selected, use web search as default
        if not agents_to_use:
            agents_to_use.append("web_search")
            rationale["web_search"] = "Default agent for general questions"
            
        return agents_to_use, rationale
    
    def _synthesize_response(self, question: str, agent_responses: List[tuple]) -> str:
        """Synthesize a final response from agent responses"""
        if not agent_responses:
            return "No relevant information found."
        
        # If Groq is available, use it for response synthesis
        if self.groq_client is not None:
            try:
                return self._llm_synthesize_response(question, agent_responses)
            except Exception as e:
                print(f"LLM response synthesis failed, using simple concatenation: {e}")
        
        # Fallback to simple concatenation
        response_parts = []
        for agent_name, response in agent_responses:
            if agent_name == "pdf_rag":
                response_parts.append(f"From PDF documents: {response.get('summary', '')}")
            elif agent_name == "web_search":
                response_parts.append(f"From web search: {response.get('summary', '')}")
            elif agent_name == "arxiv":
                response_parts.append(f"From ArXiv papers: {response.get('summary', '')}")
                
        return ". ".join(response_parts) if response_parts else "No relevant information found."
    
    def _llm_synthesize_response(self, question: str, agent_responses: List[tuple]) -> str:
        """Use LLM to synthesize a coherent response"""
        if self.groq_client is None:
            # Fallback to simple concatenation
            response_parts = []
            for agent_name, response in agent_responses:
                if agent_name == "pdf_rag":
                    response_parts.append(f"From PDF documents: {response.get('summary', '')}")
                elif agent_name == "web_search":
                    response_parts.append(f"From web search: {response.get('summary', '')}")
                elif agent_name == "arxiv":
                    response_parts.append(f"From ArXiv papers: {response.get('summary', '')}")
                    
            return ". ".join(response_parts) if response_parts else "No relevant information found."
        
        # Prepare the context for the LLM
        context_parts = []
        for agent_name, response in agent_responses:
            if agent_name == "pdf_rag":
                context_parts.append(f"PDF Document Information: {response.get('summary', '')}")
            elif agent_name == "web_search":
                context_parts.append(f"Web Search Results: {response.get('summary', '')}")
            elif agent_name == "arxiv":
                context_parts.append(f"ArXiv Papers: {response.get('summary', '')}")
        
        context = "\n\n".join(context_parts)
        
        prompt = f"""
        Based on the following information, provide a comprehensive answer to the question.
        
        Question: {question}
        
        Information:
        {context}
        
        Please synthesize a clear, concise, and helpful response based on the provided information.
        """
        
        try:
            chat_completion = self.groq_client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model="llama-3.1-70b-versatile",  # Updated model
                temperature=0.3,
                max_tokens=500,
            )
            
            response_content = chat_completion.choices[0].message.content
            return response_content if response_content is not None else "No relevant information found."
        except Exception as e:
            print(f"Error in LLM response synthesis: {e}")
            # Fallback to simple concatenation
            response_parts = []
            for agent_name, response in agent_responses:
                if agent_name == "pdf_rag":
                    response_parts.append(f"From PDF documents: {response.get('summary', '')}")
                elif agent_name == "web_search":
                    response_parts.append(f"From web search: {response.get('summary', '')}")
                elif agent_name == "arxiv":
                    response_parts.append(f"From ArXiv papers: {response.get('summary', '')}")
                    
            return ". ".join(response_parts) if response_parts else "No relevant information found."
    
    def get_logs(self) -> List[LogEntry]:
        """Return all logs"""
        return self.logs
    
    def _load_logs(self):
        """Load logs from file"""
        try:
            if os.path.exists(self.log_file):
                with open(self.log_file, "r") as f:
                    logs_data = json.load(f)
                    for log_data in logs_data:
                        # Convert timestamp string to datetime object
                        log_data["timestamp"] = datetime.fromisoformat(log_data["timestamp"])
                        self.logs.append(LogEntry(**log_data))
        except Exception as e:
            print(f"Error loading logs: {e}")
    
    def _save_logs(self):
        """Save logs to file"""
        try:
            # Create logs directory if it doesn't exist
            os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
            
            # Convert logs to JSON-serializable format
            logs_data = []
            for log in self.logs:
                log_dict = log.dict()
                # Convert datetime to string for JSON serialization
                log_dict["timestamp"] = log_dict["timestamp"].isoformat()
                logs_data.append(log_dict)
            
            with open(self.log_file, "w") as f:
                json.dump(logs_data, f, indent=2)
        except Exception as e:
            print(f"Error saving logs: {e}")