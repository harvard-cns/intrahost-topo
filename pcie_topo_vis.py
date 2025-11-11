from graphviz import Digraph
from typing import List, Dict, Optional
from os.path import basename
from collections import deque
from pcie_node import PcieNode
from pcie_topo_gen import get_pcie_trees
from collections import defaultdict
from device_resolver import get_class_name
import argparse
import os


"""
get_node_id
get_node_label
"""


def get_node_id(n: PcieNode) -> str:
    """
    In a Graphviz Diagraph, the id of a node must be unique.
    In PCIe topology, sysfs paths are unique to nodes.
    The id for a given PcieNode `n` is its sysfs path.
    "/", ":", ".", and "-" cannot be in a valid Graphviz node id.
    """

    uns_p = n.path
    san_p = (
        uns_p.replace("/", "_").replace(":", "_").replace(".", "_").replace("-", "_")
    )
    return san_p


def is_3d_controller(n: PcieNode):
    return n.class_ is not None and n.class_.startswith("0x0302")


def is_network_controller(n: PcieNode):
    return n.class_ is not None and n.class_.startswith("0x02")


def is_ethernet_controller(n: PcieNode):
    return n.class_ is not None and n.class_.startswith("0x0200")


def is_infiniband_controller(n: PcieNode):
    return n.class_ is not None and n.class_.startswith("0x0207")


def get_class_label(n: PcieNode) -> str:
    if is_other_sys_peripheral(n):
        return "Other system peripheral"
    elif is_3d_controller(n):
        return "3D controller"
    elif is_bridge(n):
        return "PCI Bridge"
    elif is_ethernet_controller(n):
        return "Ethernet Controller"
    elif is_infiniband_controller(n):
        return "Infiniband Controller"
    elif is_network_controller(n):
        return "Network controller"
    else:
        # Try to get class name from lspci
        if n.vendor and n.device:
            class_name = get_class_name(n.vendor, n.device, n.class_)
            if class_name:
                return class_name
        return n.class_ if n.class_ is not None else ""


def get_node_label(n: PcieNode) -> str:
    """
    Unlike node IDs, labels are displayed
    in the rendered Graphviz image.
    """

    label = (basename(n.path)[5:]) + "\n"
    
    from device_resolver import get_device_resolver
    resolver = get_device_resolver()
    
    #Vendor
    if n.vendor is not None:
        vendor_name = resolver.get_vendor_name(n.vendor)
        label += f"vendor: {vendor_name} \n"
    
    #Device
    if n.device is not None:
        device_name = resolver.get_device_name(n.vendor, n.device)
        label += f"device: {device_name} \n"
    
    #System identifiers (network interfaces, RDMA devices, GPU indices)
    from system_identifiers import get_system_resolver
    sys_resolver = get_system_resolver()
    
    netdev, rdma, gpu_idx, nvme = sys_resolver.get_all_identifiers(n.path)
    
    #Add network interface
    if netdev:
        label += f"iface: {netdev} \n"
    
    #Add RDMA
    if rdma:
        label += f"rdma: {rdma} \n"
    
    #Add GPU index
    if gpu_idx is not None:
        label += f"GPU: {gpu_idx} \n"
    
    #Add NVMe device
    if nvme:
        label += f"nvme: {nvme} \n"
    
    # Other items
    label += (
        f"curr_lnk_s: {n.current_link_speed} \n"
        if n.current_link_speed is not None
        else ""
    )
    label += f"max_lnk_s: {n.max_link_speed} \n" if n.max_link_speed is not None else ""
    label += (
        f"curr_lnk_w: {n.current_link_width} \n"
        if n.current_link_width is not None
        else ""
    )
    label += f"max_lnk_w: {n.max_link_width} \n" if n.max_link_width is not None else ""
    label += f"cls: {get_class_label(n)} \n" if n.class_ is not None else ""

    return label


"""
get_node_parent
get_node_siblings
get_node_mf_siblings
"""


def get_node_parent(root: PcieNode, node: PcieNode) -> Optional[PcieNode]:
    """
    Returns the parent for node `node` in
    tree with root `root`.

    If `node` does not have a parent or
    `node` parent is not found in tree
    with root `root`, `None` is returned.
    """

    if root is node:
        return None

    for child in root.children:
        if child is node:
            return root

        parent = get_node_parent(child, node)
        if parent:
            return parent

    return None


def get_node_siblings(root: PcieNode, node: PcieNode) -> Optional[List[PcieNode]]:
    """
    Returns `node` siblings in tree with
    root `root` including `node`.

    Returns `None` if `node` has no parent.
    """
    parent = get_node_parent(root, node)

    if parent is None:
        return None

    return parent.children


def get_node_mf_siblings(root: PcieNode, node: PcieNode) -> Optional[List[PcieNode]]:
    """
    Returns the siblings of `node` that correspond to the same
    physical device including `node`, i.e., siblings that
    differ in function.

    Returns `None` if `node` has no siblings.
    """
    siblings = get_node_siblings(root, node)
    if siblings is None:
        return None

    node_basename = basename(node.path)
    prefix = node_basename[:-1]
    same_device_siblings = []

    for s in siblings:
        s_basename = basename(s.path)
        if s_basename.startswith(prefix):
            same_device_siblings.append(s)

    return same_device_siblings


"""
is_bridge
is_switch
is_synth_mf
is_mf_bridge
"""


def is_other_sys_peripheral(n: PcieNode):
    return n.class_ is not None and n.class_.startswith("0x0880")


def is_bridge(node: PcieNode):
    return node.class_ is not None and node.class_.startswith("0x0604")


def is_switch(node: PcieNode):
    if not is_bridge(node):
        return False

    bridge_children_count = 0
    for c in node.children:
        if is_bridge(c):
            bridge_children_count += 1

    return bridge_children_count > 1


def is_synth_mf(node: PcieNode):
    return node.path.endswith("x")


def is_mf_switch(node: PcieNode):
    if not is_synth_mf(node):
        return False

    bridges = get_mf_switch_downstream_bridges(node)
    non_bridges = get_mf_switch_downstream_nonbridges(node)
    return len(bridges) >= 1 and len(non_bridges) >= 1


"""
get_mf_bridge_bridges
get_mf_bridge_nonbridges
"""


def get_mf_switch_downstream_bridges(node: PcieNode):
    bridges = []
    for child in node.children:
        if is_bridge(child):
            bridges.append(child)
    return bridges


def get_mf_switch_downstream_nonbridges(node: PcieNode):
    non_bridges = []
    for child in node.children:
        if not is_bridge(child):
            non_bridges.append(child)
    return non_bridges


"""
add_synth_mf_nodes
"""


def add_synth_mf_nodes(root: PcieNode) -> None:
    for child in root.children:
        add_synth_mf_nodes(child)

    if root.children == []:
        return

    processed_children = set()
    new_children = []

    for child in root.children:
        if child in processed_children:
            continue

        multifunction_siblings = get_node_mf_siblings(root, child)
        if multifunction_siblings and len(multifunction_siblings) > 1:
            prefix = basename(child.path)[:-1]
            synth_multifunction_node = PcieNode(f"{prefix}x")
            synth_multifunction_node.children = multifunction_siblings
            new_children.append(synth_multifunction_node)
            for sibling in multifunction_siblings:
                processed_children.add(sibling)
        else:
            new_children.append(child)

    root.children = new_children


"""
get_node_color
graph_tree
"""


def get_node_color(n: PcieNode) -> str:
    """Determines the fill color for a node."""

    if is_other_sys_peripheral(n):
        return "antiquewhite4"
    if is_bridge(n):
        return "lightblue"
    if is_3d_controller(n):
        return "green"
    if is_network_controller(n):
        return "aquamarine1"
    return "white"


def graph_tree(root: PcieNode, graph: Digraph) -> None:
    root_id = get_node_id(root)
    root_label = get_node_label(root)
    node_color = get_node_color(root)
    graph.node(root_id, label=root_label, style="filled", fillcolor=node_color)

    for child in root.children:
        child_id = get_node_id(child)
        graph.edge(root_id, child_id)
        graph_tree(child, graph)


"""
get_mf_clusters
get_switch_clusters
get_mf_switch_clusters
"""


def get_mf_clusters(root: PcieNode) -> Dict:
    clusters = {}

    q = deque()
    q.append(root)

    while q:
        curr = q.popleft()
        if is_synth_mf(curr):
            curr_id = get_node_id(curr)
            cluster_name = f"mf_cluster_{curr_id}"
            clusters[cluster_name] = [curr_id]
            for c in curr.children:
                c_id = get_node_id(c)
                clusters[cluster_name].append(c_id)

        for c in curr.children:
            q.append(c)

    return clusters


def get_switch_clusters(root: PcieNode) -> Dict:
    clusters = {}

    q = deque()
    q.append(root)

    while q:
        curr = q.popleft()
        if is_switch(curr):
            curr_id = get_node_id(curr)
            cluster_name = f"switch_{curr_id}"
            clusters[cluster_name] = [curr_id]
            for c in curr.children:
                if is_bridge(c):
                    c_id = get_node_id(c)
                    clusters[cluster_name].append(c_id)

        for c in curr.children:
            q.append(c)

    return clusters


def get_mf_switch_clusters(root: PcieNode) -> Dict:
    clusters = {}

    q = deque()
    q.append(root)

    while q:
        curr = q.popleft()
        if is_mf_switch(curr):
            curr_id = get_node_id(curr)
            cluster_name = f"mf_switch_{curr_id}"
            clusters[cluster_name] = [curr_id]

            bridges = get_mf_switch_downstream_bridges(curr)
            nonbridges = get_mf_switch_downstream_nonbridges(curr)

            for b in bridges:
                b_id = get_node_id(b)
                clusters[cluster_name].append(b_id)
                for c in b.children:
                    c_id = get_node_id(c)
                    clusters[cluster_name].append(c_id)

            for n in nonbridges:
                n_id = get_node_id(n)
                clusters[cluster_name].append(n_id)

        for c in curr.children:
            q.append(c)

    return clusters


def graph_pcie_topology(roots: List[PcieNode], numa: str, output_dir: str = ".") -> None:
    graph_name = f"numa_{numa}"
    graph_label = f"numa_{numa}"
    graph_format = "pdf"
    graph = Digraph(name=graph_name, filename=graph_label, format=graph_format)
    graph.attr(compound="true")
    
    # Set the output directory
    graph.directory = output_dir

    for r in roots:
        graph_tree(r, graph)

    for r in roots:
        mf_switch_clusters = get_mf_switch_clusters(r)
        for name, ids in mf_switch_clusters.items():
            with graph.subgraph(name=name) as mf_switch_cluster:
                mf_switch_cluster.attr(
                    cluster="true",
                    label=name,
                    style="filled",
                    color="lightblue",
                    pencolor="black",
                )

                for id in ids:
                    mf_switch_cluster.node(id)

    for r in roots:
        switch_clusters = get_switch_clusters(r)
        for name, ids in switch_clusters.items():
            with graph.subgraph(name=name) as switch_cluster:
                switch_cluster.attr(
                    cluster="true",
                    label=name,
                    style="filled",
                    color="lightblue",
                    pencolor="black",
                )

                for id in ids:
                    switch_cluster.node(id)

    for r in roots:
        mf_clusters = get_mf_clusters(r)
        for name, ids in mf_clusters.items():
            with graph.subgraph(name=name) as mf_cluster:
                mf_cluster.attr(
                    cluster="true",
                    label=name,
                    style="filled",
                    color="yellow",
                    pencolor="black",
                )

                for id in ids:
                    mf_cluster.node(id)

    graph.render(graph_name, view=False, cleanup=True)


if __name__ == "__main__":
    from filter_config import get_active_filters
    from mappings import filter_trees_by_classes
    
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Visualize PCIe topology and generate PDF files.")
    parser.add_argument(
        "--output-dir",
        type=str,
        default=".",
        help="Directory where PDF files will be saved (default: current directory)"
    )
    args = parser.parse_args()
    
    # Create output directory if it doesn't exist
    if args.output_dir != ".":
        os.makedirs(args.output_dir, exist_ok=True)
    
    roots = get_pcie_trees("/sys/devices")

    # Ignore childless roots.
    roots_with_children = []
    for r in roots:
        if r.children != []:
            roots_with_children.append(r)

    # Add synthetic multifunction nodes.
    for r in roots_with_children:
        add_synth_mf_nodes(r)

    """
    Apply the filters specified in the filter_config.py file.
    """
    
    active_filters = get_active_filters()
    if active_filters:
        filtered_roots = filter_trees_by_classes(roots_with_children, active_filters)
        if not filtered_roots:
            print("No trees match the active filters.")
            exit(0)
    else:
        filtered_roots = roots_with_children

    numa_roots = defaultdict(list)
    for r in filtered_roots:
        if r.numa_node is not None:
            numa_roots[r.numa_node].append(r)

    for numa, roots in numa_roots.items():
        graph_pcie_topology(roots, numa, args.output_dir)
