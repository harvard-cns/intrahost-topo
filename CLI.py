"""
PCIe Topology Visualizer with Tree-level Filtering
"""

import argparse
from filter import filter_trees_by_classes, parse_filter_classes
from PcieTopoGen import get_pcie_trees
from PcieTopoVis import graph_pcie_topology, add_synth_mf_nodes
from collections import defaultdict


def main():
    parser = argparse.ArgumentParser(description="PCIe Topology Visualizer with Tree-level Filtering")
    parser.add_argument('--filter-classes', help='Comma-separated device classes (e.g., "3D controller,ethernet controller")')    
    args = parser.parse_args()
    
    #get PCIe trees
    roots = get_pcie_trees("/sys/devices")
    roots_with_children = [r for r in roots if r.children != []]
    
    for r in roots_with_children:
        add_synth_mf_nodes(r)
    
    #apply the filtering
    if args.filter_classes:
        target_classes = parse_filter_classes(args.filter_classes)
        filtered_roots = filter_trees_by_classes(roots_with_children, target_classes)
    else:
        filtered_roots = roots_with_children
    
    if not filtered_roots:
        print("No trees contain devices matching the specified classes.")
        return
    
    #NUMA node grouping
    numa_roots = defaultdict(list)
    for root in filtered_roots:
        if root.numa_node:
            numa_roots[root.numa_node].append(root)
    
    #vizualize
    for numa, roots in numa_roots.items():
        graph_pcie_topology(roots, numa)


if __name__ == "__main__":
    main()