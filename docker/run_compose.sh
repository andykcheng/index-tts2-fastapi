#!/bin/bash

# Unset DOCKER_HOST to avoid invalid URL scheme errors
unset DOCKER_HOST

# Check if Docker daemon is running
if ! docker info > /dev/null 2>&1; then
    echo "Docker daemon not running. Attempting to start..."
    sudo systemctl start docker
    sleep 5  # Wait for Docker to start
    if ! docker info > /dev/null 2>&1; then
        echo "Failed to start Docker daemon. Please check your Docker installation."
        exit 1
    fi
fi

# Pull the image explicitly
docker pull andychenghk/indextts2-fastapi:latest

# Use 'docker compose' (V2) instead of 'docker-compose' (V1)
# This bypasses the Python library conflict causing the URLSchemeUnknown error
docker compose up -d
