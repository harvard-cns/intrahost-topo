## Usage

Check if `conda` is installed using `conda --version`. If not, install it as follows. 

1. Download the `miniconda` installer using

```
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
```

2. Run the installer using

```
bash Miniconda3-latest-Linux-x86_64.sh
```

3. Initialize `conda` using 

```
~/miniconda3/bin/conda init
```

Once the `conda` environment is active, install Graphviz using 

```
conda install -c conda-forge graphviz
```

Then, 

```
pip install graphviz
```

Finally, generate graphs using 

```
python3 PcieTopoVis.py 
```

See `numa_[i].png` for `i` is a NUMA node on the current machine. 
