#!/bin/bash

# Quick run script for CC Email Sender
# Loads API key from parent .env file and runs the sender

echo "========================================"
echo "  CC Email Sender - Quick Run"
echo "========================================"

# Load environment variables from parent .env file
if [ -f ../.env ]; then
    echo "Loading API key from ../.env"
    export $(cat ../.env | grep -v '^#' | xargs)
else
    echo "Warning: No .env file found in parent directory"
fi

# Run the email sender
python send_with_cc.py recipients.csv

echo ""
echo "✨ Done!"
