FROM nvcr.io/nvidia/cuda:12.8.1-base-ubuntu24.04

LABEL org.opencontainers.image.source=https://github.com/harvard-cns/intrahost-topo
LABEL org.opencontainers.image.description="Intra-host Topology Visualizer"
LABEL org.opencontainers.image.licenses="Apache-2.0"

# Copy package lists
COPY system-packages.txt python-requirements.txt /tmp/

# Install required systems packages including Python
RUN apt-get update && apt-get install -y \
    $(cat /tmp/system-packages.txt) \
    && rm -rf /var/lib/apt/lists/*

# Add ROCm repository and install amd-smi for AMD GPU support
RUN apt-get update && apt-get install -y wget gnupg2 && \
    mkdir -p /etc/apt/keyrings && \
    wget -q -O - https://repo.radeon.com/rocm/rocm.gpg.key | gpg --dearmor -o /etc/apt/keyrings/rocm.gpg && \
    echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/rocm.gpg] https://repo.radeon.com/rocm/apt/latest noble main" > /etc/apt/sources.list.d/rocm.list && \
    apt-get update && \
    apt-get install -y amd-smi-lib && \
    rm -rf /var/lib/apt/lists/*

# Add ROCm bin to PATH for amd-smi
ENV PATH="/opt/rocm/bin:${PATH}"

# Install Python packages
RUN pip3 install --no-cache-dir --break-system-packages -r /tmp/python-requirements.txt

# Update PCI IDs database
RUN update-pciids

# Copy the project code into the container
COPY . /app

WORKDIR /app

# Create output directory for PDF files
RUN mkdir -p /output

ENTRYPOINT ["python3", "pcie_topo_vis.py", "--output-dir", "/output"]
