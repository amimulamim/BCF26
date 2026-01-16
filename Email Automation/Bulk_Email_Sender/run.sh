#!/bin/bash

# Complete Email Campaign Runner
# This script resets the CSV columns and then sends bulk emails

echo "========================================"
echo "  Complete Email Campaign Runner"
echo "========================================"

# Load environment variables from .env file
if [ -f ../.env ]; then
    echo "Loading API key from ../.env"
    export $(cat ../.env | grep -v '^#' | xargs)
else
    echo "Warning: No .env file found in parent directory"
fi

# Default CSV file
CSV_FILE="${1:-form_response.csv}"

echo "Using CSV file: $CSV_FILE"
echo ""

# Step 1: Reset columns
echo "Step 1: Resetting 'Mail Sent' column..."
python reset_columns.py "$CSV_FILE"

if [ $? -ne 0 ]; then
    echo "✗ Error: Failed to reset columns!"
    exit 1
fi

echo "✓ Columns reset successfully"
echo ""

# Step 2: Send bulk emails
echo "Step 2: Sending bulk emails..."
python send_bulk.py "$CSV_FILE"

if [ $? -ne 0 ]; then
    echo "✗ Error: Failed to send emails!"
    exit 1
fi

echo ""
echo "========================================"
echo "  ✓ Campaign completed successfully!"
echo "========================================"
