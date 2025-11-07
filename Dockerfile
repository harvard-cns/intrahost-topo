FROM nvcr.io/nvidia/cuda:12.8.1-base-ubuntu24.04

# Install required systems packages including Python
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    pciutils \
    graphviz \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
RUN pip3 install --no-cache-dir --break-system-packages graphviz

# Copy the project code into the container
COPY . /app

WORKDIR /app

# Create output directory for PDF files
RUN mkdir -p /output

ENTRYPOINT ["python3", "pcie_topo_vis.py", "--output-dir", "/output"]
