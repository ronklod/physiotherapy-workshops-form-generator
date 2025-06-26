#!/bin/bash

echo "Starting Hebrew Physiotherapy Form Generator Frontend..."
echo "==============================================="

# Check if we're in the project root directory
if [ ! -f "frontend/package.json" ]; then
    echo "Error: Please run this script from the project root directory"
    exit 1
fi

# Change to frontend directory
cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "Installing Node.js dependencies..."
    npm install
fi

# Start the React development server
echo "Starting React development server on http://localhost:3000"
echo "Press Ctrl+C to stop the server"
echo "==============================================="
npm start 