#!/bin/bash

IMAGE_NAME="github-contribution-api"
CONTAINER_NAME="github-contribution-container"

echo "Starting deployment process..."

# Pull latest code from GitHub
echo "Pulling latest code from GitHub..."
git fetch origin
git checkout main
git pull origin main

# Stop and remove existing container
echo "Stopping and removing existing container..."
docker stop $CONTAINER_NAME 2>/dev/null
docker rm $CONTAINER_NAME 2>/dev/null

# Remove existing image
echo "Removing existing image..."
docker rmi $IMAGE_NAME 2>/dev/null

# Build new image
echo "Building new image..."
docker build -t $IMAGE_NAME -f .dockerfile .

# Run new container
echo "Starting new container..."
docker run -d --name $CONTAINER_NAME -p 9050:9050 $IMAGE_NAME

echo "Deployment completed!"

# Show container logs
echo "Container logs:"
docker logs -f $CONTAINER_NAME