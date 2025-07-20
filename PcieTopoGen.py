import os
import re
from typing import List
from PcieNode import PcieNode

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


def get_pcie_trees(path: str = "/sys/devices") -> List[PcieNode]:
    """
    Args:
        path: Sysfs path where PCIe devices are mounted.
    Returns:
        List of roots.
    """
    container_paths: List[str] = []
    try:
        with os.scandir(path) as it:
            for entry in it:
                if entry.is_dir(follow_symlinks=False) and pci_container_pattern.match(
                    entry.name
                ):
                    container_paths.append(entry.path)
    except Exception as e:
        print(f"Error getting list of containers: {e}")

    nodes: List[PcieNode] = []
    for container in container_paths:
        nodes.extend(explore_pcie_container(container))

    return nodes


if __name__ == "__main__":
    trees = get_pcie_trees("/sys/devices")

    def print_tree(root, level=0):
        indent = "    " * level
        print(f"{indent}{root.path[-12:]}")
        for child in root.children:
            print_tree(child, level + 1)

    for t in trees:
        print_tree(t)
