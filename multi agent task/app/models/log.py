from pydantic import BaseModel
from typing import List
from datetime import datetime

class LogEntry(BaseModel):
    input: str
    decision: str
    agents_called: List[str]
    documents_retrieved: List[str]
    final_answer: str
    timestamp: datetime
    
    class Config:
        # This allows the model to work with datetime objects properly
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class LogResponse(BaseModel):
    logs: List[LogEntry]