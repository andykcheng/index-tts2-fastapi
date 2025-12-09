#!/bin/bash

IMAGE_NAME="indextts-server"

echo "Building Docker image: $IMAGE_NAME..."
docker build -t $IMAGE_NAME .

echo "Build complete. You can run the container with:"
echo "docker run -p 8000:8000 $IMAGE_NAME"
