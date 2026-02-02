#!/bin/bash

echo "🔧 Setting up 3D CAD Viewer & Analyzer..."
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version

# Create virtual environment (optional but recommended)
echo ""
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo ""
echo "Installing Python packages..."
pip install -r requirements_cad.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "To run the application:"
echo "1. Activate virtual environment: source venv/bin/activate"
echo "2. Run the app: streamlit run cad_viewer_app.py"
echo ""
