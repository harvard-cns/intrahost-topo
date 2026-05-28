#! /bin/bash

# This script will create a pod that will run the topo-vis-container and then copy the output files to the client.
# Usage: ./run_job_pod.sh <node-name> [--request-nvidia-gpus <N>] [--request-amd-gpus <N>] [--request-rdma <resource_key: count>]

nvidia_gpu_count=""
amd_gpu_count=""
rdma_resource=""
NODE_NAME=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --request-nvidia-gpus)
            nvidia_gpu_count="$2"
            shift 2
            ;;
        --request-amd-gpus)
            amd_gpu_count="$2"
            shift 2
            ;;
        --request-rdma)
            rdma_resource="$2"
            shift 2
            ;;
        *)
            if [ -z "$NODE_NAME" ]; then
                NODE_NAME="$1"
            else
                echo "Error: Unknown argument '$1'"
                echo "Usage: $0 <node-name> [--request-nvidia-gpus <N>] [--request-amd-gpus <N>] [--request-rdma <resource_key: count>]"
                exit 1
            fi
            shift
            ;;
    esac
done

if [ -z "$NODE_NAME" ]; then
    echo "Usage: $0 <node-name> [--request-nvidia-gpus <N>] [--request-amd-gpus <N>] [--request-rdma <resource_key: count>]"
    echo ""
    echo "Arguments:"
    echo "  <node-name>                          Name of the Kubernetes node to deploy the pod on"
    echo "  --request-nvidia-gpus <N>            Optional: Number of NVIDIA GPUs to request (omitted if not specified)"
    echo "  --request-amd-gpus <N>               Optional: Number of AMD GPUs to request (omitted if not specified)"
    echo "  --request-rdma <resource_key: count> Optional: RDMA resource to request, e.g. \"rdma/shared_ib: 1\" (omitted if not specified)"
    exit 1
fi

TEMP_YAML="job-pod-temp.yaml"

# Cleanup function
cleanup() {
  echo "Cleaning up..."
  kubectl delete pod host-topo-job 2>/dev/null || true
  rm -f "$TEMP_YAML"
}

# Set trap to cleanup on exit
trap cleanup EXIT

# Build sed command using '|' as delimiter to avoid conflicts with '/' in resource names
sed_cmd="s|REPLACE_NODE_NAME|$NODE_NAME|"

# Handle NVIDIA GPU: substitute if provided, delete lines if not
if [ -n "$nvidia_gpu_count" ]; then
    sed_cmd="$sed_cmd;s|REPLACE_NVIDIA_GPU_COUNT|$nvidia_gpu_count|"
else
    sed_cmd="$sed_cmd;/nvidia.com\/gpu:/d"
fi

# Handle AMD GPU: substitute if provided, delete lines if not
if [ -n "$amd_gpu_count" ]; then
    sed_cmd="$sed_cmd;s|REPLACE_AMD_GPU_COUNT|$amd_gpu_count|"
else
    sed_cmd="$sed_cmd;/amd.com\/gpu:/d"
fi

# Handle RDMA: substitute placeholder with full resource string if provided, delete line if not
if [ -n "$rdma_resource" ]; then
    sed_cmd="$sed_cmd;s|REPLACE_RDMA_RESOURCE|$rdma_resource|"
else
    sed_cmd="$sed_cmd;/REPLACE_RDMA_RESOURCE/d"
fi

# If no resources requested at all, remove the entire resources block
if [ -z "$nvidia_gpu_count" ] && [ -z "$amd_gpu_count" ] && [ -z "$rdma_resource" ]; then
    sed_cmd="$sed_cmd;/^    resources:$/d;/^      requests:$/d;/^      limits:$/d"
fi

# Build resource info message
resource_info=""
if [ -n "$nvidia_gpu_count" ]; then
    resource_info="$nvidia_gpu_count NVIDIA GPU(s)"
fi
if [ -n "$amd_gpu_count" ]; then
    [ -n "$resource_info" ] && resource_info="$resource_info, "
    resource_info="${resource_info}$amd_gpu_count AMD GPU(s)"
fi
if [ -n "$rdma_resource" ]; then
    [ -n "$resource_info" ] && resource_info="$resource_info, "
    resource_info="${resource_info}$rdma_resource"
fi

echo "Applying pod configuration for node: $NODE_NAME"
if [ -n "$resource_info" ]; then
    echo "  Requesting: $resource_info"
fi

# Create a temporary YAML with substitutions applied
sed -e "$sed_cmd" job-pod.yaml > "$TEMP_YAML"
kubectl apply -f "$TEMP_YAML"

# Wait for the pod to be scheduled (assigned to a node)
echo "Waiting for pod to be scheduled..."
kubectl wait --for=condition=PodScheduled pod/host-topo-job --timeout=300s

# For DEBUGGING: Check for image pull errors in all containers
# echo "Checking for image pull errors..."
# for i in {1..30}; do
#   sleep 2
#   IMAGE_PULL_ERRORS=$(kubectl get pod host-topo-job -o jsonpath='{.status.containerStatuses[*].state.waiting.reason}' 2>/dev/null)
#   if echo "$IMAGE_PULL_ERRORS" | grep -q "ImagePullBackOff\|ErrImagePull"; then
#     echo "Error: Failed to pull container image(s)"
#     kubectl describe pod host-topo-job | grep -A 10 "Events:"
#     exit 1
#   fi
  
#   # Check if both containers are ready or at least running
#   CONTAINERS_READY=$(kubectl get pod host-topo-job -o jsonpath='{.status.containerStatuses[*].ready}' 2>/dev/null)
#   if [ ! -z "$CONTAINERS_READY" ]; then
#     # At least one status exists, images are pulling or pulled
#     break
#   fi
# done

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

sleep 2

# Show container logs for debugging
echo ""
echo "=== topo-vis-container logs ==="
kubectl logs host-topo-job -c topo-vis-container
echo "=== end logs ==="
echo ""

# List all files in /output for debugging
echo "Contents of /output directory:"
kubectl exec host-topo-job -c helper-container -- ls -la /output
echo ""

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
