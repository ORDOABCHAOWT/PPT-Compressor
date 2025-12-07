#!/bin/bash

# PPT Compressor - Automator App Creator
# This script creates a macOS application using Automator

set -e

echo "=========================================="
echo "  PPT Compressor App Builder"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Get the current directory
CURRENT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_NAME="PPT Compressor"
APP_PATH="$CURRENT_DIR/${APP_NAME}.app"

echo -e "${BLUE}📦 Creating application bundle...${NC}"
echo ""

# Check if app already exists
if [ -d "$APP_PATH" ]; then
    echo -e "${YELLOW}⚠  Application already exists. Removing old version...${NC}"
    rm -rf "$APP_PATH"
fi

# Create the app bundle structure
mkdir -p "$APP_PATH/Contents/MacOS"
mkdir -p "$APP_PATH/Contents/Resources"

echo -e "${GREEN}✓ Created app bundle structure${NC}"

# Create Python wrapper script first
cat > "$APP_PATH/Contents/Resources/run_gui.py" << 'WRAPPER_EOF'
#!/usr/bin/env python3
import os
import sys

# Change to Resources directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Import and run the GUI
try:
    import ppt_compressor_gui
    ppt_compressor_gui.main()
except Exception as e:
    import tkinter as tk
    from tkinter import messagebox
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("启动错误", f"无法启动PPT Compressor:\n\n{str(e)}")
    sys.exit(1)
WRAPPER_EOF

chmod +x "$APP_PATH/Contents/Resources/run_gui.py"

# Create the launcher script - proper bash script for GUI with ARM64 support
cat > "$APP_PATH/Contents/MacOS/launcher" << 'LAUNCHER_EOF'
#!/bin/bash

# Get the Resources directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
RESOURCES_DIR="$DIR/../Resources"

cd "$RESOURCES_DIR"

# Find Python3
if [ -x "/usr/local/bin/python3" ]; then
    PYTHON="/usr/local/bin/python3"
elif [ -x "/opt/homebrew/bin/python3" ]; then
    PYTHON="/opt/homebrew/bin/python3"
elif [ -x "/usr/bin/python3" ]; then
    PYTHON="/usr/bin/python3"
else
    PYTHON="python3"
fi

# Execute the wrapper script with ARM64 architecture on Apple Silicon
exec arch -arm64 "$PYTHON" "$RESOURCES_DIR/run_gui.py"
LAUNCHER_EOF

chmod +x "$APP_PATH/Contents/MacOS/launcher"

echo -e "${GREEN}✓ Created launcher script${NC}"

# Copy icon to Resources
if [ -f "$CURRENT_DIR/PPTCompressor.icns" ]; then
    cp "$CURRENT_DIR/PPTCompressor.icns" "$APP_PATH/Contents/Resources/AppIcon.icns"
    echo -e "${GREEN}✓ Added application icon${NC}"
else
    echo -e "${YELLOW}⚠  Icon file not found. App will use default icon.${NC}"
fi

# Copy all necessary files to Resources
cp "$CURRENT_DIR/compress_v3.sh" "$APP_PATH/Contents/Resources/"
cp "$CURRENT_DIR/ppt_compressor_v3.py" "$APP_PATH/Contents/Resources/"
cp "$CURRENT_DIR/ppt_compressor_gui.py" "$APP_PATH/Contents/Resources/"
cp "$CURRENT_DIR/launch_ppt_compressor.sh" "$APP_PATH/Contents/Resources/"
cp "$CURRENT_DIR/requirements_v3.txt" "$APP_PATH/Contents/Resources/"

# Copy icon files if they exist
if [ -f "$CURRENT_DIR/icon_128.png" ]; then
    cp "$CURRENT_DIR/icon_128.png" "$APP_PATH/Contents/Resources/"
fi

# Make scripts executable
chmod +x "$APP_PATH/Contents/Resources/compress_v3.sh"
chmod +x "$APP_PATH/Contents/Resources/ppt_compressor_v3.py"
chmod +x "$APP_PATH/Contents/Resources/ppt_compressor_gui.py"
chmod +x "$APP_PATH/Contents/Resources/launch_ppt_compressor.sh"

echo -e "${GREEN}✓ Copied application files${NC}"

# Create Info.plist
cat > "$APP_PATH/Contents/Info.plist" << PLIST_EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>launcher</string>
    <key>CFBundleIconFile</key>
    <string>AppIcon</string>
    <key>CFBundleIdentifier</key>
    <string>com.whitney.pptcompressor</string>
    <key>CFBundleName</key>
    <string>PPT Compressor</string>
    <key>CFBundleDisplayName</key>
    <string>PPT Compressor</string>
    <key>CFBundleVersion</key>
    <string>3.0</string>
    <key>CFBundleShortVersionString</key>
    <string>3.0</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleSignature</key>
    <string>????</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.13</string>
    <key>NSHighResolutionCapable</key>
    <true/>
    <key>LSUIElement</key>
    <string>0</string>
    <key>CFBundleDocumentTypes</key>
    <array>
        <dict>
            <key>CFBundleTypeExtensions</key>
            <array>
                <string>pptx</string>
                <string>ppt</string>
            </array>
            <key>CFBundleTypeName</key>
            <string>PowerPoint Presentation</string>
            <key>CFBundleTypeRole</key>
            <string>Viewer</string>
        </dict>
    </array>
</dict>
</plist>
PLIST_EOF

echo -e "${GREEN}✓ Created Info.plist${NC}"

echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}✓ Application created successfully!${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "Location: ${YELLOW}$APP_PATH${NC}"
echo ""
echo -e "${BLUE}📋 Next steps:${NC}"
echo -e "1. Test the app by double-clicking: ${YELLOW}$APP_PATH${NC}"
echo -e "2. If it works, copy to Applications:"
echo -e "   ${YELLOW}cp -r \"$APP_PATH\" /Applications/${NC}"
echo ""
echo -e "${BLUE}💡 Tips:${NC}"
echo "- The app will open Terminal and run the compression tool"
echo "- Make sure Python 3 and dependencies are installed"
echo "- Run option 7 in the menu to install dependencies"
echo ""
