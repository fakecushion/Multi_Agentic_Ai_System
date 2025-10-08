from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from app.api.routes import router

app = FastAPI(title="Multi-Agent AI System")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Multi-Agent AI System API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)