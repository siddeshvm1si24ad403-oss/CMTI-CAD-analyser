#!/bin/bash

echo "🍎 macOS Quick Setup for 3D CAD Viewer"
echo "======================================"
echo ""

# Check if conda is available
if command -v conda &> /dev/null
then
    echo "✅ Conda detected - Using conda installation (recommended)"
    echo ""
    
    # Create conda environment
    echo "Creating conda environment..."
    conda create -n cad_viewer python=3.11 -y
    
    echo ""
    echo "Activating environment..."
    eval "$(conda shell.bash hook)"
    conda activate cad_viewer
    
    echo ""
    echo "Installing packages via conda..."
    conda install -c conda-forge streamlit trimesh numpy pillow scipy -y
    
    echo ""
    echo "✅ Installation complete!"
    echo ""
    echo "To run the app:"
    echo "  conda activate cad_viewer"
    echo "  streamlit run cad_viewer_app.py"
    
else
    echo "⚠️  Conda not found - Using pip with simplified requirements"
    echo ""
    
    # Check Python version
    echo "Checking Python version..."
    python3 --version
    
    # Create virtual environment
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
    
    # Install simplified requirements (without scipy)
    echo ""
    echo "Installing packages (simplified version)..."
    pip install -r requirements_cad_simple.txt
    
    echo ""
    echo "✅ Installation complete!"
    echo ""
    echo "To run the app:"
    echo "  source venv/bin/activate"
    echo "  streamlit run cad_viewer_app.py"
fi

echo ""
echo "📝 Note: If you encounter any issues, check INSTALL_MACOS.md"
