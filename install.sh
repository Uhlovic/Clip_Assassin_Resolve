#!/bin/bash

echo "========================================"
echo "  CLIP ASSASSIN v1.1 - DaVinci Resolve"
echo "  Cuts. Without mercy."
echo "========================================"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Try to find Python
if command -v python3 &> /dev/null; then
    echo -e "${GREEN}✓${NC} Python3 found! Starting Clip Assassin..."
    echo ""
    python3 clip_assassin.py
elif command -v python &> /dev/null; then
    echo -e "${GREEN}✓${NC} Python found! Starting Clip Assassin..."
    echo ""
    python clip_assassin.py
else
    echo -e "${YELLOW}⚠${NC} Python not found in PATH."
    echo ""
    echo "Please install Python 3.6+ or use DaVinci Resolve's Python:"
    echo ""
    echo "macOS path example:"
    echo '"/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Frameworks/Python.framework/Versions/3.6/bin/python3" clip_assassin.py'
    echo ""
fi
