#!/bin/bash

# Test script for the /generate-opus, /generate-wav, /generate-opus-json, and /generate-wav-json endpoints
# Assumes the FastAPI server is running on http://localhost:8803
BITRATE=40
# Sample JSON payload
JSON_DATA='{"text": "Hello! World!!", "voice_id": "segment", "bitrate": '"$BITRATE"'}'

# Test /generate-opus
URL_OPUS="http://localhost:8804/generate-opus"
OUTPUT_FILE_OPUS="test_output.opus"

echo "Testing /generate-opus..."
echo "Sending POST request to $URL_OPUS..."
echo "Payload: $JSON_DATA"

curl -X POST "$URL_OPUS" \
     -H "Content-Type: application/json" \
     -d "$JSON_DATA" \
     -o "$OUTPUT_FILE_OPUS"

if [ -s "$OUTPUT_FILE_OPUS" ]; then
    echo "Success! Opus file saved as $OUTPUT_FILE_OPUS"
    echo "You can play it with a media player that supports Opus format."
else
    echo "Error: Failed to generate or download the Opus file."
fi

echo ""

# Test /generate-wav
URL_WAV="http://localhost:8804/generate-wav"
OUTPUT_FILE_WAV="test_output.wav"

echo "Testing /generate-wav..."
echo "Sending POST request to $URL_WAV..."
echo "Payload: $JSON_DATA"

curl -X POST "$URL_WAV" \
     -H "Content-Type: application/json" \
     -d "$JSON_DATA" \
     -o "$OUTPUT_FILE_WAV"

if [ -s "$OUTPUT_FILE_WAV" ]; then
    echo "Success! WAV file saved as $OUTPUT_FILE_WAV"
    echo "You can play it with a media player that supports WAV format."
else
    echo "Error: Failed to generate or download the WAV file."
fi

echo ""

# Test /generate-opus-json
URL_OPUS_JSON="http://localhost:8804/generate-opus-json"
OUTPUT_FILE_OPUS_JSON="test_output_opus.json"

echo "Testing /generate-opus-json..."
echo "Sending POST request to $URL_OPUS_JSON..."
echo "Payload: $JSON_DATA"

curl -X POST "$URL_OPUS_JSON" \
     -H "Content-Type: application/json" \
     -d "$JSON_DATA" \
     -o "$OUTPUT_FILE_OPUS_JSON"

if [ -s "$OUTPUT_FILE_OPUS_JSON" ]; then
    echo "Success! JSON response saved as $OUTPUT_FILE_OPUS_JSON"
else
    echo "Error: Failed to save the JSON response for Opus."
fi

echo ""

# Test /generate-wav-json
URL_WAV_JSON="http://localhost:8804/generate-wav-json"
OUTPUT_FILE_WAV_JSON="test_output_wav.json"

echo "Testing /generate-wav-json..."
echo "Sending POST request to $URL_WAV_JSON..."
echo "Payload: $JSON_DATA"

curl -X POST "$URL_WAV_JSON" \
     -H "Content-Type: application/json" \
     -d "$JSON_DATA" \
     -o "$OUTPUT_FILE_WAV_JSON"

if [ -s "$OUTPUT_FILE_WAV_JSON" ]; then
    echo "Success! JSON response saved as $OUTPUT_FILE_WAV_JSON"
else
    echo "Error: Failed to save the JSON response for WAV."
fi
