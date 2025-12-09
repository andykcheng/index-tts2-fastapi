#!/bin/bash

if [ -z "$1" ]; then
    echo "Usage: $0 <image_name_or_id>"
    exit 1
fi

INPUT_NAME="$1"

# Resolve full image ID to ensure we catch all containers (handles short IDs and tags)
FULL_IMAGE_ID=$(docker inspect --format="{{.Id}}" "$INPUT_NAME" 2>/dev/null)

if [ -z "$FULL_IMAGE_ID" ]; then
    echo "Image '$INPUT_NAME' not found locally."
    exit 1
fi

echo "Found image ID: $FULL_IMAGE_ID"
echo "Cleaning up..."

# Find containers using this image (using full ID is more reliable)
CONTAINERS=$(docker ps -a --filter "ancestor=$FULL_IMAGE_ID" --format "{{.ID}}")

if [ -n "$CONTAINERS" ]; then
    echo "Stopping and removing containers using image $INPUT_NAME..."
    echo "$CONTAINERS" | xargs -r docker stop
    echo "$CONTAINERS" | xargs -r docker rm
else
    echo "No containers found using image $INPUT_NAME."
fi

# Remove the image
echo "Removing image: $INPUT_NAME"
docker rmi "$INPUT_NAME"

echo "Cleanup complete."
