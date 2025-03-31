import os
import re
import concurrent.futures
from PCIeDeviceNode import PCIeDeviceNode

# Container pattern matches directories like "pci0000:00"
pci_container_pattern = re.compile(r"^pci[0-9a-fA-F]{4}:[0-9a-fA-F]{2}$")
# Device pattern matches PCIe device nodes like "0000:e1:00.0"
pci_device_pattern = re.compile(r"^[0-9a-fA-F]{4}:[0-9a-fA-F]{2}:[0-1][0-9a-fA-F]\.[0-7]$")

def explore_pcie_nodes(path: str) -> list:
    """
    Recursively explore the directory at 'path' for PCIe device nodes.
    Returns a list of PCIeDeviceNode objects.
    """
    nodes = []
    try:
        with os.scandir(path) as it:
            for entry in it:
                if entry.is_dir(follow_symlinks=False):
                    name = entry.name
                    full_path = entry.path
                    if pci_device_pattern.match(name):
                        # This directory represents a PCIe device node.
                        node = PCIeDeviceNode(full_path)
                        # Recursively search for any children beneath this device node.
                        node.children = explore_pcie_nodes(full_path)
                        nodes.append(node)
                    # Even if the directory name doesn't match exactly a PCIe node,
                    # if it starts with "pci", it may be a container.
                    elif name.startswith("pci"):
                        nodes.extend(explore_pcie_nodes(full_path))
    except Exception as e:
        print(f"Error exploring {path}: {e}")
    return nodes

def build_pcie_tree(path="/sys/devices") -> PCIeDeviceNode:
    """
    Build the PCIe topology tree using the given base path.
    
    - Creates a root node for the base path.
    - Scans for container directories (e.g., pci0000:00) in the base directory.
    - Uses a thread pool to concurrently explore the PCIe nodes within each container.
    - Returns the root node with its children populated.
    """
    # Create the root node for the entire tree.
    root = PCIeDeviceNode(path)
    root.children = []
    
    # Pre-filter: get a list of container directories in the base path.
    container_paths = []
    try:
        with os.scandir(path) as it:
            for entry in it:
                if entry.is_dir(follow_symlinks=False) and pci_container_pattern.match(entry.name):
                    container_paths.append(entry.path)
    except Exception as e:
        print(f"Error scanning base directory {path}: {e}")
    
    # Use a thread pool to explore each container concurrently.
    nodes = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        future_to_path = {executor.submit(explore_pcie_nodes, container_path): container_path 
                          for container_path in container_paths}
        for future in concurrent.futures.as_completed(future_to_path):
            try:
                result_nodes = future.result()
                nodes.extend(result_nodes)
            except Exception as e:
                print(f"Error processing container {future_to_path[future]}: {e}")
    
    root.children = nodes
    return root

if __name__ == "__main__":
    tree_root = build_pcie_tree("/sys/devices")
    
    def print_tree(node, level=0):
        indent = "          " * level
        print(f"{indent}{node}")
        for child in node.children:
            print_tree(child, level + 1)
    
    print_tree(tree_root)
