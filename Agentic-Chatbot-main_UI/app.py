from fastapi import FastAPI
from api.chat import app as chat_app
import os
from sqlalchemy import create_engine

# Create the main FastAPI app
app = FastAPI(
    title="Agentic Chatbot API",
    description="An intelligent airline support chatbot with agent-based routing",
    version="1.0.0"
)

# Include the chat router
app.include_router(chat_app, prefix="/api/v1")

@app.get("/")
def root():
    return {
        "message": "Agentic Chatbot API is running",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "agentic-chatbot"}
