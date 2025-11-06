FROM nvcr.io/nvidia/cuda:12.8.1-base-ubuntu24.04

# Install system packages including Python
RUN apt-get update && apt-get install -y \
    git \
    python3 \
    python3-pip \
    python3-venv \
    graphviz \
    pciutils \
    lshw \
    iproute2 \
    net-tools \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
RUN pip3 install --no-cache-dir --break-system-packages graphviz

