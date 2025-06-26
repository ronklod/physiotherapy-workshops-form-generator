#!/bin/bash

echo "Starting Hebrew Physiotherapy Form Generator Backend..."
echo "=============================================="

# Check if we're in the backend directory
if [ ! -f "backend/main.py" ]; then
    echo "Error: Please run this script from the project root directory"
    exit 1
fi

# Change to backend directory
cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Start the FastAPI server
echo "Starting FastAPI server on http://localhost:8000"
echo "Press Ctrl+C to stop the server"
echo "=============================================="
uvicorn main:app --reload --host 0.0.0.0 --port 8000 