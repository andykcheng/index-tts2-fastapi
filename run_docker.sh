#!/bin/bash

IMAGE_NAME="indextts-server"
CONTAINER_NAME="indextts-container"

# Stop and remove any existing container with the same name
echo "Stopping old container..."
docker stop $CONTAINER_NAME 2>/dev/null || true
docker rm $CONTAINER_NAME 2>/dev/null || true

echo "Starting new container..."
# --gpus all: Pass GPU access to container
# -p 8000:8000: Map host port 8000 to container port 8000
# -v $(pwd)/outputs:/app/outputs: Mount local outputs folder to container
docker run -d \
    --name $CONTAINER_NAME \
    --gpus all \
    -p 8000:8000 \
    -v "$(pwd)/outputs:/app/outputs" \
    $IMAGE_NAME

echo "Container started!"
echo "You can follow the logs with: docker logs -f $CONTAINER_NAME"
echo "Test the endpoint with: ./test_generate.sh"
