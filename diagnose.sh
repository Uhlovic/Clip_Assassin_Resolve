#!/bin/bash

# Clip Assassin - Resolve Connection Diagnostics
# Shell script for macOS/Linux

echo ""
echo "========================================================================"
echo "  ⚔️ CLIP ASSASSIN - Running Diagnostics"
echo "========================================================================"
echo ""

# Set Resolve API paths (in case they're needed)
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    export RESOLVE_SCRIPT_API="/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting"
    export PYTHONPATH="$RESOLVE_SCRIPT_API/Modules:$PYTHONPATH"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    export RESOLVE_SCRIPT_API="/opt/resolve/Developer/Scripting"
    export PYTHONPATH="$RESOLVE_SCRIPT_API/Modules:$PYTHONPATH"
fi

# Try python3 first, then python
if command -v python3 &> /dev/null; then
    python3 diagnose_resolve.py
elif command -v python &> /dev/null; then
    python diagnose_resolve.py
else
    echo "ERROR: Python is not installed or not in PATH"
    echo "Please install Python 3.10 from https://www.python.org/downloads/"
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi

# Keep terminal open
read -p "Press Enter to exit..."
