#!/bin/bash

echo "Starting Hebrew Physiotherapy Form Generator Full Stack..."
echo "=============================================="

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "Error: npm is not installed. Please install Node.js and npm."
    exit 1
fi

# Build the frontend
echo "Building React frontend..."
cd frontend
npm install
npm run build
cd ..

# Start the backend (which now serves the frontend)
echo "Starting backend server with integrated frontend..."
./start-backend.sh
