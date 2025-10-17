#!/bin/bash

echo "Setting up Hector mesh..."

# Ensure venv and pip are available
sudo apt update
sudo apt install -y python3-venv python3-full

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Launch Hector
echo "Launching Hector..."
PYTHONIOENCODING=utf-8 python main.py