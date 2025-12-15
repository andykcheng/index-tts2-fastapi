#!/bin/bash

echo "Stopping running containers..."
docker stop $(docker ps -q --filter ancestor=index-tts-fastapi) 2>/dev/null

echo "Removing old image..."
docker rmi index-tts-fastapi 2>/dev/null

echo "Building new image..."
docker build -t index-tts-fastapi .

echo "Tagging image for Docker Hub..."
docker tag index-tts-fastapi andychenghk/indextts2-fastapi

echo "Pushing to Docker Hub..."
docker push andychenghk/indextts2-fastapi

echo "Done!"
