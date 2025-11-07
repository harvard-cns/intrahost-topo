#!/bin/bash

# Check for the argument --local to build the image locally
if [ "$1" == "--local" ]; then
  image_name="host-topo-vis"
  if ! docker image inspect $image_name > /dev/null 2>&1; then
    echo "Docker image '$image_name' not found locally. Building image..."
    docker build -t $image_name .
  else
    echo "Docker image '$image_name' already exists locally. Skipping build."
  fi
else
  echo "Pre-build docker image is currently not available."
  echo "Please run with --local to build the image locally and run the container."
  exit 1
  # TODO: provide pre-built image's repository and tag
  # image_name="harvard-cns/host-topo-vis:latest"
fi

echo "-----------------------------------------------------"
echo "Running the container with the image: $image_name"
echo "-----------------------------------------------------"
# Run the container with automatic cleanup
docker run --rm \
    -v $(pwd):/output \
    --gpus=all \
    --network=host \
    $image_name
echo "Done!"
