#!/bin/bash

# PPT Compressor - Install to Applications
# This script installs the app to /Applications folder

set -e

echo "=========================================="
echo "  Install PPT Compressor to Applications"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

CURRENT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_NAME="PPT Compressor"
SOURCE_APP="$CURRENT_DIR/${APP_NAME}.app"
DEST_APP="/Applications/${APP_NAME}.app"

# Check if source app exists
if [ ! -d "$SOURCE_APP" ]; then
    echo -e "${RED}✗ Error: Application not found at: $SOURCE_APP${NC}"
    echo -e "${YELLOW}Please run ./create_app.sh first to build the application.${NC}"
    exit 1
fi

echo -e "${BLUE}📦 Source: $SOURCE_APP${NC}"
echo -e "${BLUE}📍 Destination: $DEST_APP${NC}"
echo ""

# Check if app already exists in Applications
if [ -d "$DEST_APP" ]; then
    echo -e "${YELLOW}⚠  PPT Compressor already exists in Applications folder.${NC}"
    read -p "Do you want to replace it? (y/n): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}Installation cancelled.${NC}"
        exit 0
    fi
    echo -e "${BLUE}Removing old version...${NC}"
    rm -rf "$DEST_APP"
fi

# Copy the app to Applications
echo -e "${BLUE}Installing application...${NC}"
cp -R "$SOURCE_APP" "$DEST_APP"

echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}✓ Installation completed successfully!${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "${GREEN}PPT Compressor is now installed in your Applications folder!${NC}"
echo ""
echo -e "${BLUE}🚀 How to use:${NC}"
echo "1. Open Launchpad or Applications folder"
echo "2. Click on 'PPT Compressor' icon"
echo "3. The tool will open in Terminal"
echo ""
echo -e "${BLUE}📋 First-time setup:${NC}"
echo "- Select option 7 to install dependencies"
echo "- Make sure Python 3 is installed"
echo "- Install oxipng for best compression: brew install oxipng"
echo ""
echo -e "${GREEN}Enjoy compressing your PPT files! 🎉${NC}"
echo ""
