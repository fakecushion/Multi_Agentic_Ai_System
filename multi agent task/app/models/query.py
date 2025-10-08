from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class QueryRequest(BaseModel):
    question: str
    context: Optional[str] = None

class AgentInfo(BaseModel):
    name: str
    rationale: str

class DocumentInfo(BaseModel):
    id: str
    title: str
    content: str

class QueryResponse(BaseModel):
    answer: str
    agents_used: List[AgentInfo]
    documents_retrieved: List[DocumentInfo]
    timestamp: datetime