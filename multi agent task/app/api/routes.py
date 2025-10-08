from fastapi import APIRouter, UploadFile, File, Form
from typing import Optional
from app.agents.controller import ControllerAgent
from app.models.query import QueryRequest, QueryResponse
from app.models.log import LogResponse
import os

router = APIRouter()

# Initialize controller
controller = ControllerAgent()

@router.post("/ask", response_model=QueryResponse)
async def ask_question(query: QueryRequest):
    """Ask a question to the multi-agent system"""
    response = await controller.process_query(query)
    return response

@router.post("/upload_pdf")
async def upload_pdf(file: UploadFile = File(...)):
    """Upload a PDF file for RAG processing"""
    # Create uploads directory if it doesn't exist
    os.makedirs("uploads", exist_ok=True)
    
    # Save the uploaded file
    file_path = f"uploads/{file.filename}"
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    # Process the PDF with RAG agent
    result = await controller.process_pdf(file_path)
    
    return {"message": "PDF uploaded and processed successfully", "result": result}

@router.get("/logs", response_model=LogResponse)
async def get_logs():
    """Get all logs from the system"""
    logs = controller.get_logs()
    return LogResponse(logs=logs)