#! /bin/bash

# This script will create a pod that will run the topo-vis-container and then copy the output files to the client.
# Usage: ./run_job_pod.sh <node-name>

if [ -z "$1" ]; then
  echo "Error: Node name is required"
  echo "Usage: $0 <node-name>"
  exit 1
fi

NODE_NAME="$1"
TEMP_YAML="job-pod-temp.yaml"

# Create a temporary YAML file with the specified node name
sed "s/nodeName: \".*\"/nodeName: \"$NODE_NAME\"/" job-pod.yaml > "$TEMP_YAML"

echo "Applying pod configuration for node: $NODE_NAME"
kubectl apply -f "$TEMP_YAML"

# Wait for the pod to be ready (both containers running)
kubectl wait --for=condition=ready pod/host-topo-job --timeout=300s

# Wait a bit for the topo-vis-container to finish generating the PDFs
# (The helper container keeps the pod alive for file copying)
sleep 10

# Copy the output files from the helper container (which has access to the shared volume)
echo "Copying output PDF files to current directory"
kubectl cp host-topo-job:/output/numa_0.pdf numa_0.pdf -c helper-container
kubectl cp host-topo-job:/output/numa_1.pdf numa_1.pdf -c helper-container

# Delete the pod
kubectl delete pod host-topo-job

# Clean up temporary YAML file
rm -f "$TEMP_YAML"
