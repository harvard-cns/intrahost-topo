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
