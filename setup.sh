#!/bin/bash

echo "Hebrew Physiotherapy Form Generator Setup"
echo "========================================"
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    echo "Please install Python 3 and try again."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "Error: Node.js is required but not installed."
    echo "Please install Node.js and try again."
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"
echo "✓ Node.js found: $(node --version)"
echo ""

# Setup Backend
echo "Setting up Backend..."
echo "-------------------"

cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
else
    echo "Virtual environment already exists"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "✓ Backend setup complete"
echo ""

# Setup Frontend
cd ../frontend

echo "Setting up Frontend..."
echo "--------------------"

# Install Node.js dependencies
echo "Installing Node.js dependencies..."
npm install

echo "✓ Frontend setup complete"
echo ""

# Make scripts executable
cd ..
chmod +x start-backend.sh
chmod +x start-frontend.sh

echo "Setup Complete! 🎉"
echo "=================="
echo ""
echo "To start the application:"
echo "1. Start the backend: ./start-backend.sh"
echo "2. In another terminal, start the frontend: ./start-frontend.sh"
echo ""
echo "Then open http://localhost:3000 in your browser"
echo ""
echo "The backend API will be available at http://localhost:8000"
echo "API documentation: http://localhost:8000/docs" 