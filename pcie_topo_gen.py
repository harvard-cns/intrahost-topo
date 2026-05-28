import os
import re  # Regular expression
from typing import List
from pcie_node import PcieNode

pci_container_pattern = re.compile(
    r"^pci[0-9a-fA-F]{4}:[0-9a-fA-F]{2}$"
)  # E.g., "pci0000:00"
pci_node_pattern = re.compile(
    r"^[0-9a-fA-F]{4}:[0-9a-fA-F]{2}:[0-1][0-9a-fA-F]\.[0-7]$"
)  # E.g., "0000:e1:00.0"


def explore_pcie_container(path: str) -> List[PcieNode]:
    """
    Args:
        path: Path to container.
    Return:
        List of nodes found in container.
    """
    nodes: List[PcieNode] = []
    try:
        with os.scandir(path) as it:
            for entry in it:
                if not entry.is_dir(follow_symlinks=False):
                    continue

                entry_name = entry.name
                if pci_node_pattern.match(entry_name):
                    entry_path = entry.path
                    node = PcieNode(entry_path)
                    node.children = explore_pcie_container(entry_path)
                    nodes.append(node)
    except Exception as e:
        print(f"Error exploring {path}: {e}")

    return nodes


def _discover_pci_containers(path: str) -> List[str]:
    """
    Discover PCI containers (pciXXXX:XX directories) by following symlinks
    in /sys/bus/pci/devices/ and walking up to find the container parent.
    Falls back to scanning the top level of `path` directly.
    """
    containers: set = set()

    # Primary: follow /sys/bus/pci/devices/ symlinks to find containers
    bus_pci_dir = "/sys/bus/pci/devices"
    if os.path.exists(bus_pci_dir):
        try:
            for dev in os.listdir(bus_pci_dir):
                real_path = os.path.realpath(os.path.join(bus_pci_dir, dev))
                parent = os.path.dirname(real_path)
                while parent and parent != "/":
                    if pci_container_pattern.match(os.path.basename(parent)):
                        containers.add(parent)
                        break
                    parent = os.path.dirname(parent)
        except Exception as e:
            print(f"Error discovering PCI containers from {bus_pci_dir}: {e}")

    # Fallback: scan top level of the sysfs devices path
    if not containers:
        try:
            with os.scandir(path) as it:
                for entry in it:
                    if entry.is_dir(follow_symlinks=False) and pci_container_pattern.match(
                        entry.name
                    ):
                        containers.add(entry.path)
        except Exception as e:
            print(f"Error scanning {path}: {e}")

    return sorted(containers)


def get_pcie_trees(path: str = "/sys/devices") -> List[PcieNode]:
    """
    Args:
        path: Sysfs path where PCIe devices are mounted.
    Returns:
        List of roots.
    """
    containers = _discover_pci_containers(path)

    if not containers:
        print(f"  No PCI containers found in {path}", flush=True)
    else:
        print(f"  Found {len(containers)} PCI container(s): {[os.path.basename(c) for c in containers]}", flush=True)

    nodes: List[PcieNode] = []
    for container in containers:
        container_nodes = explore_pcie_container(container)
        if not container_nodes:
            print(f"  {os.path.basename(container)}: no PCI nodes found", flush=True)
        nodes.extend(container_nodes)

    return nodes


"""
if __name__ == "__main__":
    trees = get_pcie_trees("/sys/devices")

    def print_tree(root, level=0):
        indent = "    " * level
        print(f"{indent}{root.path[-12:]}")
        for child in root.children:
            print_tree(child, level + 1)

    for t in trees:
        print_tree(t)
"""
