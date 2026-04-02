#!/bin/bash

# OpenShift Architecture Diagrams - Setup Script
# This script automates the initial setup process

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "========================================="
echo "OpenShift Architecture Diagrams - Setup"
echo "========================================="
echo ""

# Check Python version
echo "Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or later."
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✓ Found Python $PYTHON_VERSION"

# Check if graphviz is installed
echo ""
echo "Checking for Graphviz..."
if ! command -v dot &> /dev/null; then
    echo "⚠️  Graphviz is not installed."
    echo ""
    echo "Install it with one of the following commands:"
    echo "  Fedora/RHEL: sudo dnf install graphviz"
    echo "  Ubuntu/Debian: sudo apt-get install graphviz"
    echo "  macOS: brew install graphviz"
    echo ""
    read -p "Would you like to attempt automatic installation? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        make install-graphviz
    else
        echo "Please install Graphviz manually before continuing."
        exit 1
    fi
else
    echo "✓ Graphviz is installed"
fi

# Create virtual environment
echo ""
echo "Creating Python virtual environment..."
if [ -d "venv" ]; then
    echo "⚠️  Virtual environment already exists. Skipping creation."
else
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment and install dependencies
echo ""
echo "Installing Python dependencies..."
source venv/bin/activate
pip install --upgrade pip -q
pip install -r requirements.txt -q
echo "✓ Dependencies installed"

# Create output directory
echo ""
echo "Creating output directory..."
mkdir -p output
echo "✓ Output directory ready"

# Test diagram generation
echo ""
echo "Testing diagram generation..."
python3 diagrams/openshift/basic-cluster.py

if [ -f "output/openshift-basic-cluster.png" ]; then
    echo "✓ Test diagram generated successfully!"
else
    echo "❌ Test diagram generation failed."
    exit 1
fi

# Summary
echo ""
echo "========================================="
echo "✓ Setup complete!"
echo "========================================="
echo ""
echo "Next steps:"
echo "  1. Activate the virtual environment:"
echo "     source venv/bin/activate"
echo ""
echo "  2. Generate all diagrams:"
echo "     make generate-all"
echo ""
echo "  3. Create your own diagrams:"
echo "     cp templates/diagram_template.py diagrams/openshift/my-diagram.py"
echo ""
echo "  4. View generated diagrams:"
echo "     ls -lh output/"
echo ""
echo "See README.md for more information."
echo ""
