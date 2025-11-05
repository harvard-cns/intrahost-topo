FROM mcr.microsoft.com/devcontainers/python:3

# Install system packages
RUN apt-get update && apt-get install -y \
    graphviz \
    pciutils \
    lshw \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
RUN pip3 install --no-cache-dir graphviz

