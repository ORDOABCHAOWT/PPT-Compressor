#!/bin/bash

# PPT Compressor v3.0 - Launcher Script
# This script launches the PPT compression tool in a new Terminal window

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Change to the script directory
cd "$SCRIPT_DIR"

# Clear the terminal for a clean start
clear

# Run the compression tool
./compress_v3.sh
