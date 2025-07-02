#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FastAPI Backend for Hebrew Physiotherapy Workshops Form Generator
"""

import io
import os
import tempfile
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv

from hebrew_form_processor import HebrewFormProcessor

# Load environment variables from .env file
load_dotenv()

# Pydantic models for request/response
class ProcessTextRequest(BaseModel):
    text: str
    activity_type: Optional[str] = None  # User-selected activity type
    date: Optional[str] = None  # User-entered Hebrew date


class ParticipantInfo(BaseModel):
    name: str = ""
    id: str = ""
    receipt_number: str = ""
    amount: str = ""


class ProcessTextResponse(BaseModel):
    activity_type: Optional[str]
    participants: List[ParticipantInfo]
    total_participants: int
    success: bool
    message: str


# FastAPI app initialization
app = FastAPI(
    title="Hebrew Physiotherapy Workshops Form Generator",
    description="API for processing Hebrew text and generating Word documents with Groq AI integration",
    version="2.1.0"
)

# Define the path to the React build directory
# The path is relative to the backend directory since that's where the server runs from
FRONTEND_BUILD_PATH = Path(__file__).parent.parent / "frontend" / "build"

# Mount the static files from the React build directory
app.mount("/static", StaticFiles(directory=str(FRONTEND_BUILD_PATH / "static")), name="static")


# CORS middleware to allow React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint - serves the React frontend."""
    # Serve the index.html from the React build directory
    index_path = FRONTEND_BUILD_PATH / "index.html"
    
    if not index_path.exists():
        # If frontend isn't built, provide API info instead
        groq_status = "enabled" if os.getenv('GROQ_API_KEY') else "disabled (set GROQ_API_KEY environment variable)"
        return {
            "message": "Hebrew Physiotherapy Workshops Form Generator API",
            "version": "2.1.0",
            "groq_ai_integration": groq_status,
            "environment": os.getenv('ENVIRONMENT', 'development'),
            "endpoints": {
                "POST /process-text": "Process Hebrew text and extract participant information",
                "POST /generate-document": "Generate and download Word document",
                "GET /health": "Health check"
            },
            "frontend_status": "Not built. Please run 'npm run build' in the frontend directory.",
            "features": [
                "Intelligent Hebrew text processing with Groq AI (Llama 3.3 70B)",
                "User-selectable activity types and custom dates",
                "Fallback regex extraction for structured text",
                "Professional Word document generation",
                "Activity type detection",
                "Hebrew RTL formatting support"
            ]
        }
        
    # Read and serve the index.html file
    with open(index_path, "r") as f:
        html_content = f.read()
        
    return HTMLResponse(content=html_content)


@app.post("/api/process-text", response_model=ProcessTextResponse)
async def process_text(request: ProcessTextRequest):
    """
    Process Hebrew text and extract participant information using Groq AI.
    
    Args:
        request: ProcessTextRequest containing the Hebrew text, activity type, and date
        
    Returns:
        ProcessTextResponse with extracted information
    """
    try:
        if not request.text.strip():
            raise HTTPException(status_code=400, detail="Text cannot be empty")
        
        # Create processor with Groq API key from environment
        groq_api_key = os.getenv('GROQ_API_KEY')
        processor = HebrewFormProcessor(groq_api_key=groq_api_key)
        
        # Process the text
        result = processor.process_text(request.text)
        
        # Override activity type if user selected one
        if request.activity_type:
            # Map dropdown values to full Hebrew text
            activity_mapping = {
                "לאחר לידה": "התעמלות לאחר לידה",
                "הריון": "התעמלות הריון"
            }
            result['activity_type'] = activity_mapping.get(request.activity_type, request.activity_type)
        
        # Convert participants to Pydantic models
        participants = [
            ParticipantInfo(**participant) for participant in result['participants']
        ]
        
        return ProcessTextResponse(
            activity_type=result['activity_type'],
            participants=participants,
            total_participants=result['total_participants'],
            success=True,
            message="Text processed successfully using AI-powered extraction"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing text: {str(e)}")


@app.post("/api/generate-document")
async def generate_document(request: ProcessTextRequest):
    """
    Generate and return a Word document from Hebrew text using Groq AI.
    
    Args:
        request: ProcessTextRequest containing the Hebrew text, activity type, and date
        
    Returns:
        StreamingResponse with the Word document
    """
    try:
        if not request.text.strip():
            raise HTTPException(status_code=400, detail="Text cannot be empty")
        
        # Create processor with Groq API key from environment
        groq_api_key = os.getenv('GROQ_API_KEY')
        processor = HebrewFormProcessor(groq_api_key=groq_api_key)
        
        # Process the text
        result = processor.process_text(request.text)
        
        # Override activity type if user selected one
        if request.activity_type:
            activity_mapping = {
                "לאחר לידה": "התעמלות לאחר לידה",
                "הריון": "התעמלות הריון"
            }
            result['activity_type'] = activity_mapping.get(request.activity_type, request.activity_type)
        
        if not result['participants']:
            raise HTTPException(
                status_code=400, 
                detail="No participant information found in the text. Please check the text format or try with more detailed information."
            )
        
        # Create temporary file for the document
        with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as tmp_file:
            temp_path = tmp_file.name
        
        try:
            # Generate the Word document with custom title
            custom_title = None
            if request.activity_type and request.date:
                custom_title = f"{request.activity_type} - {request.date}"
            
            processor.create_word_document(temp_path, custom_title=custom_title)
            
            # Read the file content
            with open(temp_path, 'rb') as file:
                document_content = file.read()
            
            # Generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            activity_suffix = "post_birth" if "לאחר לידה" in str(result['activity_type']) else "pregnancy"
            filename = f"physiotherapy_form_{activity_suffix}_{timestamp}.docx"
            
            # Create streaming response
            return StreamingResponse(
                io.BytesIO(document_content),
                media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.unlink(temp_path)
                
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating document: {str(e)}")


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    groq_status = "available" if os.getenv('GROQ_API_KEY') else "not configured"
    
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "environment": os.getenv('ENVIRONMENT', 'development'),
        "groq_ai": groq_status,
        "capabilities": {
            "hebrew_processing": True,
            "ai_extraction": bool(os.getenv('GROQ_API_KEY')),
            "regex_fallback": True,
            "word_generation": True,
            "custom_titles": True
        }
    }


@app.get("/api/setup-help")
async def setup_help():
    """Provide setup instructions for Groq API."""
    return {
        "message": "Groq API Setup Instructions",
        "steps": [
            "1. Get your Groq API key from https://console.groq.com/",
            "2. Create a .env file in the backend directory",
            "3. Add: GROQ_API_KEY=your-api-key-here",
            "4. Restart the backend server",
            "5. The API will automatically use Groq for intelligent text extraction"
        ],
        "current_status": {
            "groq_api_key_set": bool(os.getenv('GROQ_API_KEY')),
            "fallback_available": True,
            "environment": os.getenv('ENVIRONMENT', 'development')
        },
        "note": "The system will work with regex fallback even without Groq API key, but AI extraction provides much better results for natural Hebrew text.",
        "model": "llama-3.3-70b-versatile"
    }


@app.get("/api/info")
async def api_info():
    """API information endpoint."""
    groq_status = "enabled" if os.getenv('GROQ_API_KEY') else "disabled (set GROQ_API_KEY environment variable)"
    
    return {
        "message": "Hebrew Physiotherapy Workshops Form Generator API",
        "version": "2.1.0",
        "groq_ai_integration": groq_status,
        "environment": os.getenv('ENVIRONMENT', 'development'),
        "endpoints": {
            "POST /api/process-text": "Process Hebrew text and extract participant information",
            "POST /api/generate-document": "Generate and download Word document",
            "GET /api/health": "Health check"
        },
        "features": [
            "Intelligent Hebrew text processing with Groq AI (Llama 3.3 70B)",
            "User-selectable activity types and custom dates",
            "Fallback regex extraction for structured text",
            "Professional Word document generation",
            "Activity type detection",
            "Hebrew RTL formatting support",
            "Integrated frontend serving"
        ]
    }


@app.get("/{full_path:path}")
async def serve_frontend(full_path: str, request: Request):
    """
    Serve the React frontend for any other routes.
    This enables client-side routing with React Router.
    """
    # Check if the path is an API route or a static file
    if full_path.startswith("api/") or full_path == "":
        # For API routes, pass through to the appropriate endpoint
        raise HTTPException(status_code=404, detail="API endpoint not found")
        
    # For all other routes, serve the index.html from React build
    index_path = FRONTEND_BUILD_PATH / "index.html"
    
    if not index_path.exists():
        return {"message": "Frontend not built. Please run 'npm run build' in the frontend directory."}
        
    with open(index_path, "r") as f:
        html_content = f.read()
        
    return HTMLResponse(content=html_content)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)