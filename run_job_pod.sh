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

# Wait for the pod to be scheduled (assigned to a node)
echo "Waiting for pod to be scheduled..."
kubectl wait --for=condition=PodScheduled pod/host-topo-job --timeout=300s

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

# List the output files (get just the filenames, not full paths)
echo "Listing generated PDF files..."
output_files=$(kubectl exec host-topo-job -c helper-container -- find /output -name "*.pdf" -type f -exec basename {} \;)

if [ -z "$output_files" ]; then
  echo "Error: No PDF files found in /output directory"
  exit 1
fi

echo -e "Found PDF files:\n${output_files}"

# Copy the output files from the helper container (which has access to the shared volume)
for file in $output_files; do
  echo "Copying $file to ${NODE_NAME}_$file"
  kubectl cp host-topo-job:/output/$file ${NODE_NAME}_$file -c helper-container
done

echo "Done!"
