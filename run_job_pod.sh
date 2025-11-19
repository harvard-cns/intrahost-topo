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

# Cleanup function
cleanup() {
  echo "Cleaning up..."
  kubectl delete pod host-topo-job 2>/dev/null || true
  rm -f "$TEMP_YAML"
}

# Set trap to cleanup on exit
trap cleanup EXIT

# Create a temporary YAML file with the specified node name
sed "s/nodeName: \".*\"/nodeName: \"$NODE_NAME\"/" job-pod.yaml > "$TEMP_YAML"

echo "Applying pod configuration for node: $NODE_NAME"
kubectl apply -f "$TEMP_YAML"

# Wait for the pod to be ready (both containers running)
kubectl wait --for=condition=ready pod/host-topo-job --timeout=300s

# Wait for the topo-vis-container to finish generating the PDFs
# (The helper container keeps the pod alive for file copying)
echo "Waiting for topo-vis-container to complete..."
while true; do
  sleep 2  # check every 2 seconds
  CONTAINER_STATE=$(kubectl get pod host-topo-job -o jsonpath='{.status.containerStatuses[?(@.name=="topo-vis-container")].state}')
  if echo "$CONTAINER_STATE" | grep -q "terminated"; then
    EXIT_CODE=$(kubectl get pod host-topo-job -o jsonpath='{.status.containerStatuses[?(@.name=="topo-vis-container")].state.terminated.exitCode}')
    if [ "$EXIT_CODE" = "0" ]; then
      echo "topo-vis-container completed successfully"
      break
    else
      echo "Error: topo-vis-container failed with exit code $EXIT_CODE"
      exit 1
    fi
  fi
done

# Copy the output files from the helper container (which has access to the shared volume)
echo "Copying output PDF files to current directory: numa_0.pdf and numa_1.pdf"
kubectl cp host-topo-job:/output/numa_0.pdf numa_0.pdf -c helper-container
kubectl cp host-topo-job:/output/numa_1.pdf numa_1.pdf -c helper-container
