FROM nvcr.io/nvidia/cuda:12.8.1-base-ubuntu24.04

# Copy package lists from root directory
COPY system-packages.txt python-requirements.txt /tmp/

# Install system packages including Python (shared + dev tools)
RUN apt-get update && apt-get install -y \
    $(cat /tmp/system-packages.txt) \
    git \
    python3-venv \
    lshw \
    iproute2 \
    net-tools \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
RUN pip3 install --no-cache-dir --break-system-packages -r /tmp/python-requirements.txt

# Update PCI IDs database
RUN update-pciids
