#!/bin/sh

# Activate the virtual environment
source .venv/bin/activate

# Set environment variables
export FLASK_DEBUG=1
export FLASK_APP=main.py

# Run the Flask development server
python3 -m flask run --port 10000