## Usage

Install `conda`. Find instructions at `https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html`. 

Create a `conda` environment named `host-topo` using `conda env create -f conda_env.yaml`. 

Activate the environment using `conda activate host-topo`.

### Running the Visualizer

Run `python3 PcieTopoVis.py` to generate PCIe topology visualizations.

### Filtering

To filter which device types are included in the visualization:

1. Open `filter_config.py` in a text editor
2. Set any filter variable to `True` to include trees containing that device class
3. Set to `False` to exclude trees containing that device class
4. Run `python3 PcieTopoVis.py` again

**Note**: When `show_all = True`, all other filter settings are ignored and every node will be displayed.


### Device Name Resolution

The visualizer automatically converts raw PCI vendor/device IDs into human-readable names:

### Output

See `numa_[i].png` for `i` is a NUMA node on the current machine. 
