We intend to create a tree that represents the hierarchy of PCIe devices as in the `/sys/devices/` folder. 

First, access folders with names of the form `pci<domain>:<bus>`. 

Create PCIeNode objects for each folder of the form `<domain>:<bus>:<device>.<function>`.


