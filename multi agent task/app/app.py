"""
Gradio interface for the Multi-Agent AI System
This interface is optimized for Hugging Face Spaces deployment
"""
import gradio as gr
import requests
import os
from typing import List, Dict, Any
import time

# Get the backend URL (for HF Spaces, this will be the same server)
BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")

def ask_question(question: str) -> str:
    """Ask a question to the multi-agent system"""
    try:
        response = requests.post(
            f"{BACKEND_URL}/ask",
            json={"question": question},
            timeout=30
        )
        if response.status_code == 200:
            data = response.json()
            # Format the response nicely
            result = f"**Answer:**\n{data['answer']}\n\n"
            result += "**Agents Used:**\n"
            for agent in data['agents_used']:
                result += f"- {agent['name']}: {agent['rationale']}\n"
            return result
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Error connecting to backend: {str(e)}"

def upload_pdf(file_obj) -> str:
    """Upload a PDF file for processing"""
    if file_obj is None:
        return "Please select a PDF file to upload."
    
    try:
        with open(file_obj.name, 'rb') as f:
            files = {'file': f}
            response = requests.post(
                f"{BACKEND_URL}/upload_pdf",
                files=files,
                timeout=30
            )
        
        if response.status_code == 200:
            data = response.json()
            return f"**PDF Upload Result:**\n{data['message']}"
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Error uploading PDF: {str(e)}"

def get_logs() -> str:
    """Get system logs"""
    try:
        response = requests.get(f"{BACKEND_URL}/logs", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if not data['logs']:
                return "No logs available."
            
            # Format the logs nicely
            result = "**Recent System Logs:**\n\n"
            # Show last 5 logs
            for i, log in enumerate(reversed(data['logs'][-5:])):
                result += f"**Log Entry {i+1}:**\n"
                result += f"Input: {log['input']}\n"
                result += f"Decision: {log['decision']}\n"
                result += f"Agents Called: {', '.join(log['agents_called'])}\n"
                result += f"Time: {log['timestamp']}\n"
                result += "-" * 50 + "\n"
            return result
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Error retrieving logs: {str(e)}"

# Create the Gradio interface
with gr.Blocks(title="Multi-Agent AI System") as demo:
    gr.Markdown("""
    # Multi-Agent AI System
    
    This system dynamically decides which agent(s) to call for your query.
    It includes specialized agents for PDF documents, web search, and academic papers.
    """)
    
    with gr.Tab("Ask Question"):
        with gr.Row():
            with gr.Column():
                question_input = gr.Textbox(
                    label="Enter your question",
                    placeholder="What would you like to know?",
                    lines=3
                )
                ask_btn = gr.Button("Get Answer")
            with gr.Column():
                answer_output = gr.Markdown(label="Answer")
        ask_btn.click(
            fn=ask_question,
            inputs=question_input,
            outputs=answer_output
        )
    
    with gr.Tab("Upload PDF"):
        with gr.Row():
            with gr.Column():
                pdf_input = gr.File(label="Upload PDF", file_types=[".pdf"])
                upload_btn = gr.Button("Process PDF")
            with gr.Column():
                pdf_output = gr.Markdown(label="Result")
        upload_btn.click(
            fn=upload_pdf,
            inputs=pdf_input,
            outputs=pdf_output
        )
    
    with gr.Tab("System Logs"):
        with gr.Row():
            with gr.Column():
                logs_btn = gr.Button("Load Logs")
            with gr.Column():
                logs_output = gr.Markdown(label="Logs")
        logs_btn.click(
            fn=get_logs,
            inputs=[],
            outputs=logs_output
        )

# For local development
if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7861)  # Use port 7861