# Intra-host Topology Visualizer

A tool to discover and visualize the intra-host network topology of multi-accelerator servers running Linux. Currently, the tool only supports the PCIe interconnect. 

<!-- ## Setup

The tool uses conda to install and manage the dependencies including the `dot` binary from the [graphviz](https://graphviz.org/download/) package.

1. If you do not already have `conda`, install the minimal version (miniconda) from [here](https://docs.conda.io/en/latest/).

2. Git clone this repository and cd into it:
    ```
    git clone https://github.com/harvard-cns/intrahost-topo.git
    cd intrahost-topo
    ```
3. Create the conda environment named `host-topo` using the provided yaml file:
    ```
    conda env create -f conda_env.yaml
    ``` -->

## Usage

<!-- Activate the conda environment `host-topo`:
```
conda activate host-topo
``` -->

### Using pre-built Docker image

Simply run the following command:
```
docker run --rm -v $(pwd):/output --gpus=all --network=host ghcr.io/rajkiranjoshi/host-topo-vis:latest
```

This runs the latest pre-built Docker image of the tool. If there you encounter rate limiting issues in pulling the pre-built Docker image, you can also build and run the image locally following the instructions below.

### Using pre-built Docker image on a Kubernetes node

Simply run the provided helper script with the node name of the target server:
```
./run_job_pod.sh <node-name>
```
The helper script applies the [job-pod.yaml](./job-pod.yaml) manifest file and collects back the output PDF files.


### Building Docker image locally and then running it

1. Git clone this repository and cd into it:
    ```
    git clone https://github.com/harvard-cns/intrahost-topo.git
    cd intrahost-topo
    ```

2. Run the provided `run.sh` script:
    ```
    ./run.sh --local
    ```

This builds a Docker image called `host-topo-vis` locally and also runs it.

### Using local setup

> [!NOTE]  
> The tool assumes that CUDA drivers and toolkit are installed on the system and `nvidia-smi` is available on the PATH.


1. Install the system dependencies mentioned in `system-packages.txt`. Example command for Ubuntu/Debian-based systems:
    ```
    sudo apt update && sudo apt install -y $(cat system-packages.txt)
    ```
2. Update the PCI IDs database:
    ```
    sudo update-pciids
    ```

3. Install the Python dependencies mentioned in `python-requirements.txt` in a Python virtual environment:
    ```
    python3 -m venv venv
    source venv/bin/activate
    pip3 install -r python-requirements.txt
    ```

4. Now run the visualizer tool:
    ```
    python3 pcie_topo_vis.py --output-dir ./output
    ```

### Output

The visualizer produces two PDF files one corresponding to each NUMA node (CPU) on the server. The files are named `numa_i.pdf` for `i` is a NUMA node on the current machine. 

### Capturing PCIe topology for offline analysis

If you need to debug the topology without direct access to the server, you can export the discovered topology to a JSON IR file and load it later on another machine.

- Dump the topology to JSON:
    ```
    python3 pcie_topo_vis.py --dump-ir ./topology.json
    ```
- Render PDFs from a previously dumped JSON file:
    ```
    python3 pcie_topo_vis.py --from-ir ./topology.json --output-dir ./output
    ```

### Device Name Resolution

The visualizer automatically converts raw PCI vendor/device IDs into human-readable names using the [PCI ID database](https://pci-ids.ucw.cz/). You can customize the vendor/device names in the final output by modifying the `known_devices.json` and `known_vendors.json` files. When available, the visualizer uses names from these files instead of the PCI ID database.

### [Optional] Filtering

There can way too many PCIe trees on modern servers. By default, the tool shows all the PCIe trees. To filter which device types are included in the visualization:

1. Open `filter_config.py` in a text editor.
2. Set any filter variable to `True` to include trees containing that device class.
3. Set to `False` to exclude trees containing that device class.
4. Run `python3 pcie_topo_vis.py` again.

**Note**: When `show_all = True`, all other filter settings are ignored and every node will be displayed.


