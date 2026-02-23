#!/bin/bash

echo "Stopping running containers..."
docker stop $(docker ps -q --filter ancestor=index-tts-fastapi) 2>/dev/null

echo "Removing old image..."
docker rmi index-tts-fastapi 2>/dev/null

echo "Building new image (pulling base image, no cache)..."
# Force Docker to pull the latest base image and ignore cache so the repo clone layer is always executed.
# Also pass a timestamp build-arg as an extra cache-buster.
docker build --pull --no-cache --build-arg CACHEBUST=$(date +%s) -t index-tts-fastapi .

echo "Tagging image for Docker Hub..."
docker tag index-tts-fastapi andychenghk/indextts2-fastapi

echo "Pushing to Docker Hub..."
docker push andychenghk/indextts2-fastapi

echo "Done!"
