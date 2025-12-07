#!/bin/bash

# PPT Compressor v3.0 - Launcher Script
# This script launches the PPT compression tool GUI

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Change to the script directory
cd "$SCRIPT_DIR"

# Check if Python3 is available
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    osascript -e 'display dialog "错误: 未找到Python\n请先安装Python 3" buttons {"确定"} default button 1 with icon stop'
    exit 1
fi

# Launch the GUI
$PYTHON_CMD ppt_compressor_gui.py
