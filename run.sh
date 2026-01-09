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
  image_name="ghcr.io/rajkiranjoshi/host-topo-vis:latest"
fi

# Detect GPU type and set appropriate Docker flags
gpu_flags=""

# Check for NVIDIA GPUs
if command -v nvidia-smi &> /dev/null && nvidia-smi &> /dev/null; then
  echo "Detected NVIDIA GPU(s)"
  gpu_flags="--gpus=all"
fi

# Check for AMD GPUs (ROCm uses /dev/kfd and /dev/dri)
if [ -e /dev/kfd ]; then
  echo "Detected AMD GPU(s)"
  gpu_flags="$gpu_flags --device=/dev/kfd --device=/dev/dri --group-add video"
fi

if [ -z "$gpu_flags" ]; then
  echo "Warning: No NVIDIA or AMD GPUs detected. Running without GPU passthrough."
fi

echo "-----------------------------------------------------"
echo "Running the container with the image: $image_name"
echo "-----------------------------------------------------"
# Run the container with automatic cleanup
docker run --rm \
    -v $(pwd):/output \
    $gpu_flags \
    --network=host \
    $image_name
echo "Done!"
