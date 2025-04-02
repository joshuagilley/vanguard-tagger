#!/bin/bash

# Stop script on error
set -e  

echo "🚀 Starting Lambda local test workflow..."

# Build the Docker image
echo "🐳 Building Docker image..."
docker build -t tag-generator-image:latest .

# Build the AWS SAM Lambda function with the container image
echo "🔨 Building AWS SAM function..."
sam build --use-container --build-image tag-generator-image:latest

# Invoke the Lambda function locally using the test event
echo "⚡ Invoking Lambda function locally..."
sam local invoke TaggingServiceFunction -e event.json

echo "✅ Workflow completed successfully!"
