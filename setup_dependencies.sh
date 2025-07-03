#!/bin/bash
echo "==============================================="
echo "Asana Report Desktop App - Setup Dependencies"
echo "==============================================="

echo "Installing required packages..."
pip install -r requirements.txt

echo ""
echo "Dependencies installed successfully!"
echo ""
echo "To build the macOS desktop app, run:"
echo "python build_macos_app.py"
echo ""
echo "To run the web version, run:"
echo "streamlit run app.py"
echo ""
read -p "Press Enter to continue..."
