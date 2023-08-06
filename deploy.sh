#!/bin/bash

# Set a trap to handle Ctrl+C
trap 'kill $(jobs -p); exit' SIGINT

# Exit on any error
set -e

# Echo in color
green='\e[32m'
yellow='\e[33m'
nc='\e[0m' # No color

# Replace these with your own values
PROJECT_ID="sentiment-analysis-flask"
REGION="asia-southeast1"
SERVICE_NAME="sa-new"
IMAGE_NAME="sa-new:latest"
DOCKERFILE_PATH="."

# Start timer and set estimated execution time (in seconds)
start_time=$SECONDS
total_estimated_time=150

# Build the Docker image
echo -e "\n${yellow}Building the Docker image...${nc}"
# The --no-cache option is used in the docker build command to ensure you're building a fresh image each time without using any cached layers from previous builds.
docker build -t $IMAGE_NAME $DOCKERFILE_PATH --no-cache && echo -e "\n${green}Docker image built successfully!${nc}"

# Authenticate Docker to gcloud
echo -e "\n${yellow}Authenticating Docker to gcloud...${nc}"
gcloud auth configure-docker && echo -e "\n${green}Docker authenticated to gcloud successfully!${nc}"

# Tag the Docker image
echo -e "\n${yellow}Tagging the Docker image...${nc}"
docker tag $IMAGE_NAME gcr.io/$PROJECT_ID/$IMAGE_NAME && echo -e "\n${green}Docker image tagged successfully!${nc}"

# Push the Docker image to GCR
echo -e "\n${yellow}Pushing the Docker image to GCR...${nc}"
docker push gcr.io/$PROJECT_ID/$IMAGE_NAME && echo -e "\n${green}Docker image pushed to GCR successfully!${nc}"

# Deploy the Docker image to GCR
echo -e "\n${yellow}Deploying the Docker image to Cloud Run...${nc}"
gcloud run deploy $SERVICE_NAME --image gcr.io/$PROJECT_ID/$IMAGE_NAME --platform managed --region $REGION --allow-unauthenticated && echo -e "\n${green}Docker image deployed to Cloud Run successfully!${nc}"

# Display elapsed time
elapsed=$((SECONDS - start_time))
percentage=$((elapsed * 100 / total_estimated_time))
progress=$((percentage / 2))
printf "Elapsed time: %d seconds [%-50s] %d%%\n" $elapsed $(printf '%.0s#' $(seq 1 $progress)) $percentage

# #!/bin/bash

# # Set your project ID
# PROJECT_ID="sentiment-analysis-flask"

# # Set the service name
# SERVICE_NAME="sa-new"

# # Set the region
# REGION="asia-southeast1"

# # Set the Image name
# IMAGE_NAME="sa-new:latest"

# # Build a new Docker image locally
# echo "Building a new Docker image..."
# docker build -t $IMAGE_NAME .

# # Tag the new image for uploading to the registry
# echo "Tagging the new image..."
# docker tag $IMAGE_NAME gcr.io/$PROJECT_ID/$IMAGE_NAME

# # Push the new image to Google Cloud Registry
# echo "Pushing the new image..."
# docker push gcr.io/$PROJECT_ID/$IMAGE_NAME

# # Deploy the new image to Cloud Run
# echo "Deploying..."
# gcloud run deploy $SERVICE_NAME --image gcr.io/$PROJECT_ID/$IMAGE_NAME --port 8080 --platform managed --region $REGION --allow-unauthenticated

# echo "Deployment finished!"