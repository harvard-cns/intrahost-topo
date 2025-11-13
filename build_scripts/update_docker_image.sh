#!/bin/bash
echo "-----------------------------------------------------"
echo "Updating Docker image locally first ..."
echo "-----------------------------------------------------"
docker build -t ghcr.io/rajkiranjoshi/host-topo-vis:latest ..

echo "-----------------------------------------------------"
echo "Pushing Docker image to GitHub Container Registry ..."
echo "-----------------------------------------------------"
docker login ghcr.io
docker push ghcr.io/rajkiranjoshi/host-topo-vis:latest
docker logout ghcr.io
echo "-----------------------------------------------------"
echo "Done!"
echo "-----------------------------------------------------"
