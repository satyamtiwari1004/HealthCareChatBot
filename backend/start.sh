#!/bin/bash

# Healthcare Chatbot Backend Startup Script

echo "🏥 Starting Healthcare Chatbot Backend..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Check for environment file
if [ ! -f "../.env" ]; then
    echo "⚠️  No .env file found. Please copy .env.example to .env and add your OpenAI API key."
    exit 1
fi

# Start the server
echo "🚀 Starting FastAPI server..."
cd app && python main.py