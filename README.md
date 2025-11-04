# Intra-host Topology Visualizer

A tool to discover and visualize the intra-host network topology of multi-accelerator servers running Linux. Currently, the tool only supports the PCIe interconnect. 

## Setup

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
    ```

## Usage

Activate the conda environment `host-topo`:
```
conda activate host-topo
```

Now run the visualizer:
```
python3 PcieTopoVis.py
```

### Output

The visualizer produces two PDF files one corresponding to each NUMA node (CPU) on the server. The files are named `numa_i.pdf` for `i` is a NUMA node on the current machine. 

### Filtering

To filter which device types are included in the visualization:

1. Open `filter_config.py` in a text editor
2. Set any filter variable to `True` to include trees containing that device class
3. Set to `False` to exclude trees containing that device class
4. Run `python3 PcieTopoVis.py` again

**Note**: When `show_all = True`, all other filter settings are ignored and every node will be displayed.


### Device Name Resolution

The visualizer automatically converts raw PCI vendor/device IDs into human-readable names.


