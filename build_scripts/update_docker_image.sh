#!/bin/bash

# Get the directory of this script
curr_dir=$(dirname $(realpath $0))
root_dir=$(dirname $curr_dir)

echo "Building Docker image in $root_dir ..."
# rm output PDF files in $root_dir
rm -f $root_dir/output/*.pdf
echo "-----------------------------------------------------"
echo "Updating Docker image locally first ..."
echo "-----------------------------------------------------"
docker build -t ghcr.io/rajkiranjoshi/host-topo-vis:latest $root_dir

echo "-----------------------------------------------------"
echo "Pushing Docker image to GitHub Container Registry ..."
echo "-----------------------------------------------------"
docker login ghcr.io
docker push ghcr.io/rajkiranjoshi/host-topo-vis:latest
docker logout ghcr.io
echo "-----------------------------------------------------"
echo "Done!"
echo "-----------------------------------------------------"
