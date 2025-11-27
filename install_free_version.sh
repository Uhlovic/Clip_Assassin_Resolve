#!/bin/bash

# Clip Assassin - FREE Version Installer for macOS/Linux

echo ""
echo "======================================================================"
echo "  CLIP ASSASSIN - FREE VERSION INSTALLER"
echo "======================================================================"
echo ""
echo "This will install Clip Assassin for DaVinci Resolve FREE version"
echo "(also works with STUDIO version)"
echo ""

# Detect OS
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    DEST_DIR="/Library/Application Support/Blackmagic Design/DaVinci Resolve/Fusion/Scripts/Utility"
    echo "Detected macOS"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    DEST_DIR="/opt/resolve/Fusion/Scripts/Utility"
    echo "Detected Linux"
else
    echo "ERROR: Unsupported operating system: $OSTYPE"
    exit 1
fi

echo "Installation directory: $DEST_DIR"
echo ""
read -p "Press Enter to continue or Ctrl+C to cancel..."

# Check if destination directory exists
if [ ! -d "$DEST_DIR" ]; then
    echo ""
    echo "ERROR: Destination directory not found!"
    echo "$DEST_DIR"
    echo ""
    echo "Creating directory..."
    sudo mkdir -p "$DEST_DIR"

    if [ $? -ne 0 ]; then
        echo "Failed to create directory. Make sure DaVinci Resolve is installed."
        exit 1
    fi
fi

echo ""
echo "Installing files..."
echo ""

# Copy main script
sudo cp "clip_assassin_free.py" "$DEST_DIR/clip_assassin_free.py"
if [ $? -eq 0 ]; then
    echo "[OK] Copied clip_assassin_free.py"
else
    echo "ERROR: Failed to copy clip_assassin_free.py"
    echo "You may need to run this with sudo"
    exit 1
fi

# Copy time parser (optional)
sudo cp "time_parser.py" "$DEST_DIR/time_parser.py" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "[OK] Copied time_parser.py"
else
    echo "[!] Could not copy time_parser.py (using built-in fallback)"
fi

# Set permissions
sudo chmod +x "$DEST_DIR/clip_assassin_free.py"

echo ""
echo "======================================================================"
echo "  INSTALLATION COMPLETE!"
echo "======================================================================"
echo ""
echo "To use Clip Assassin FREE version:"
echo ""
echo "1. Open DaVinci Resolve (FREE or STUDIO)"
echo "2. Open a project"
echo "3. Import a video clip to Media Pool"
echo "4. Go to: Workspace → Scripts → Utility → clip_assassin_free"
echo ""
echo "If the script doesn't appear, restart DaVinci Resolve."
echo ""
read -p "Press Enter to exit..."
