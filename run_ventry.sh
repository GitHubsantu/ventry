#!/bin/bash
# Ventry Inventory Manager Launcher for Linux/Mac
# This script launches the Ventry application

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║   ██╗   ██╗███████╗███╗   ██╗████████╗██████╗ ██╗   ██╗    ║"
echo "║   ██║   ██║██╔════╝████╗  ██║╚══██╔══╝██╔══██╗╚██╗ ██╔╝    ║"
echo "║   ██║   ██║█████╗  ██╔██╗ ██║   ██║   ██████╔╝ ╚████╔╝     ║"
echo "║   ╚██╗ ██╔╝██╔══╝  ██║╚██╗██║   ██║   ██╔══██╗  ╚██╔╝      ║"
echo "║    ╚████╔╝ ███████╗██║ ╚████║   ██║   ██║  ██║   ██║       ║"
echo "║     ╚═══╝  ╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝   ╚═╝       ║"
echo "║                                                              ║"
echo "║           Inventory Manager - Quick Start Guide              ║"
echo "║                                                              ║"
echo "║   Developer : github.com/githubsantu                          ║"
echo "║   Website   : https://imdevops.in                              ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "Starting application..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3 from your package manager or https://www.python.org/"
    exit 1
fi

# Check if PyQt5 is installed
if ! python3 -c "import PyQt5" &> /dev/null; then
    echo "PyQt5 not found. Installing..."
    pip3 install PyQt5
fi

# Run the application
python3 main.py
