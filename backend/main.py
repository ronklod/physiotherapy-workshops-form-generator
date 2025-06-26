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

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from dotenv import load_dotenv

from hebrew_form_processor import HebrewFormProcessor

# Load environment variables from .env file
load_dotenv()

# Pydantic models for request/response
class ProcessTextRequest(BaseModel):
    text: str


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
    version="2.0.0"
)

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
    """Root endpoint with API information."""
    groq_status = "enabled" if os.getenv('GROQ_API_KEY') else "disabled (set GROQ_API_KEY environment variable)"
    
    return {
        "message": "Hebrew Physiotherapy Workshops Form Generator API",
        "version": "2.0.0",
        "groq_ai_integration": groq_status,
        "environment": os.getenv('ENVIRONMENT', 'development'),
        "endpoints": {
            "POST /process-text": "Process Hebrew text and extract participant information",
            "POST /generate-document": "Generate and download Word document",
            "GET /health": "Health check"
        },
        "features": [
            "Intelligent Hebrew text processing with Groq AI (Llama 3.3 70B)",
            "Fallback regex extraction for structured text",
            "Professional Word document generation",
            "Activity type detection",
            "Hebrew RTL formatting support"
        ]
    }


@app.post("/process-text", response_model=ProcessTextResponse)
async def process_text(request: ProcessTextRequest):
    """
    Process Hebrew text and extract participant information using Groq AI.
    
    Args:
        request: ProcessTextRequest containing the Hebrew text
        
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


@app.post("/generate-document")
async def generate_document(request: ProcessTextRequest):
    """
    Generate and return a Word document from Hebrew text using Groq AI.
    
    Args:
        request: ProcessTextRequest containing the Hebrew text
        
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
        
        if not result['participants']:
            raise HTTPException(
                status_code=400, 
                detail="No participant information found in the text. Please check the text format or try with more detailed information."
            )
        
        # Create temporary file for the document
        with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as tmp_file:
            temp_path = tmp_file.name
        
        try:
            # Generate the Word document
            processor.create_word_document(temp_path)
            
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


@app.get("/health")
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
            "word_generation": True
        }
    }


@app.get("/setup-help")
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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 