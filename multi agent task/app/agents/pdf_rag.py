import fitz  # PyMuPDF
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import os
import uuid
from typing import List, Dict

class PDFRAGAgent:
    def __init__(self):
        # Initialize sentence transformer model for embeddings
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Initialize FAISS index
        self.dimension = 384  # Dimension of the embeddings
        self.index = faiss.IndexFlatL2(self.dimension)
        
        # Store document chunks and metadata
        self.documents = []
        self.doc_metadata = []
        
        # Process sample PDFs if they exist
        self._process_sample_pdfs()
    
    def _process_sample_pdfs(self):
        """Process sample PDFs in the sample_pdfs directory"""
        sample_pdfs_dir = "sample_pdfs"
        if os.path.exists(sample_pdfs_dir):
            for filename in os.listdir(sample_pdfs_dir):
                if filename.endswith(".pdf"):
                    file_path = os.path.join(sample_pdfs_dir, filename)
                    self.process_pdf(file_path)
    
    def process_pdf(self, file_path: str) -> dict:
        """Process a PDF file, extract text, chunk it, and add to the vector store"""
        try:
            # Extract text from PDF
            doc = fitz.open(file_path)
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()
            
            # Chunk the text
            chunks = self._chunk_text(text)
            
            # Create embeddings for chunks
            embeddings = self.model.encode(chunks)
            
            # Add to FAISS index
            start_id = len(self.documents)
            self.index.add(np.array(embeddings).astype('float32'))
            
            # Store document chunks and metadata
            for i, chunk in enumerate(chunks):
                doc_id = str(uuid.uuid4())
                self.documents.append({
                    "id": doc_id,
                    "content": chunk,
                    "source": file_path
                })
                self.doc_metadata.append({
                    "id": doc_id,
                    "title": os.path.basename(file_path),
                    "chunk_index": i
                })
            
            return {
                "status": "success",
                "message": f"Processed {len(chunks)} chunks from {file_path}",
                "chunks_processed": len(chunks)
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error processing PDF: {str(e)}"
            }
    
    def _chunk_text(self, text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
        """Chunk text into smaller pieces"""
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), chunk_size - overlap):
            chunk = " ".join(words[i:i + chunk_size])
            if chunk.strip():  # Only add non-empty chunks
                chunks.append(chunk)
                
        return chunks
    
    def search(self, query: str, k: int = 3) -> dict:
        """Search for relevant documents based on the query"""
        try:
            # Create embedding for the query
            query_embedding = self.model.encode([query])
            
            # Search in FAISS index
            distances, indices = self.index.search(np.array(query_embedding).astype('float32'), k)
            
            # Retrieve relevant documents
            retrieved_docs = []
            for i, idx in enumerate(indices[0]):
                if idx < len(self.documents):
                    doc = self.documents[idx]
                    retrieved_docs.append({
                        "id": doc["id"],
                        "title": self.doc_metadata[idx]["title"],
                        "content": doc["content"],
                        "distance": float(distances[0][i])
                    })
            
            # Create a simple summary (would be replaced with LLM summarization)
            summary = " ".join([doc["content"][:200] + "..." for doc in retrieved_docs[:2]])
            
            return {
                "documents": retrieved_docs,
                "summary": summary if summary else "No relevant documents found."
            }
        except Exception as e:
            return {
                "documents": [],
                "summary": f"Error during search: {str(e)}"
            }