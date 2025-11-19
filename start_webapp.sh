#!/bin/bash

echo "=========================================="
echo "Book Cover Generator - Web App"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed."
    echo "Please install Python 3.8 or later."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "Error: pip is not installed."
    echo "Please install pip for Python 3."
    exit 1
fi

echo "✓ Python found: $(python3 --version)"
echo ""

# Check if requirements are installed
if ! python3 -c "import flask" 2>/dev/null; then
    echo "Installing dependencies..."
    pip3 install -r requirements.txt
    echo ""
fi

# Check for Ideogram API key
if [ -z "$IDEOGRAM_API_KEY" ]; then
    echo "⚠ Warning: IDEOGRAM_API_KEY environment variable not set"
    echo "The app will run in simulation mode (placeholder images)"
    echo ""
    echo "To set your API key:"
    echo "  export IDEOGRAM_API_KEY='your-api-key-here'"
    echo ""
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
    echo ""
fi

# Create necessary directories
mkdir -p projects
mkdir -p templates

echo "Starting Flask server..."
echo "----------------------------------------"
echo "Web Interface: http://localhost:5000"
echo "----------------------------------------"
echo "Press Ctrl+C to stop the server"
echo ""

# Start the Flask app
python3 app.py
