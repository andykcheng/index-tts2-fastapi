#!/bin/bash

# Test script for the /generate-opus endpoint
# Assumes the FastAPI server is running on http://localhost:8000

URL="http://localhost:8000/generate-opus"
OUTPUT_FILE="test_output.opus"

# Sample JSON payload
JSON_DATA='{"text": "Hello World!!!", "voice_id": "default"}'

echo "Sending POST request to $URL..."
echo "Payload: $JSON_DATA"

# Send the request and save the response
curl -X POST "$URL" \
     -H "Content-Type: application/json" \
     -d "$JSON_DATA" \

# Check if the file was created and has content
if [ -s "$OUTPUT_FILE" ]; then
    echo "Success! Opus file saved as $OUTPUT_FILE"
    echo "You can play it with a media player that supports Opus format."
else
    echo "Error: Failed to generate or download the Opus file."
fi
