from graphviz import Digraph
from typing import List, Dict, Optional
from collections import defaultdict
from os.path import basename

from PcieNode import PcieNode
from PcieTopoGen import get_pcie_trees


def get_node_id(n: PcieNode) -> str:
    path = n.path
    return path.replace("/", "_").replace(":", "_").replace(".", "_").replace("-", "_")


def get_node_label(n: PcieNode) -> str:
    label = (basename(n.path)) + "\n"
    label += n.class_ if n.class_ is not None else ""
    label += n.numa_node if n.numa_node is not None else ""
    return label


def get_node_parent(root: PcieNode, node: PcieNode) -> Optional[PcieNode]:
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
    parent = get_node_parent(root, node)
    if parent is None:
        return None
    return parent.children


def get_same_device_siblings(root: PcieNode, node: PcieNode) -> List[PcieNode]:
    # TODO: Review
    siblings = get_node_siblings(root, node)
    if siblings is None:
        raise Exception("Something went wrong. ")
    node_basename = basename(node.path)
    prefix = node_basename[:-1]
    same_device_siblings = []
    for s in siblings:
        s_basename = basename(s.path)
        if s_basename.startswith(prefix):
            same_device_siblings.append(s)
    return same_device_siblings


def add_synth_multifunction_nodes(root: PcieNode) -> None:
    # TODO: Review
    for child in root.children:
        add_synth_multifunction_nodes(child)

    if root.children == []:
        return

    processed_children = set()
    new_children = []

    for child in root.children:
        if child in processed_children:
            continue

        same_device_siblings = get_same_device_siblings(root, child)
        if len(same_device_siblings) > 1:
            prefix = basename(child.path)[:-2]
            synth_multifunction_node = PcieNode(f"{prefix}.x")
            synth_multifunction_node.children = same_device_siblings
            new_children.append(synth_multifunction_node)
            for sibling in same_device_siblings:
                processed_children.add(sibling)
        else:
            new_children.append(child)

    root.children = new_children


def graph_tree(root: PcieNode, graph: Digraph) -> None:
    root_id = get_node_id(root)
    root_label = get_node_label(root)

    graph.node(root_id, label=root_label)

    for child in root.children:
        child_id = get_node_id(child)
        graph.edge(root_id, child_id)
        graph_tree(child, graph)

    # The redundant traversal is the root cause of the issue.
    # Clustering should be done in a separate, single pass.
    # cluster_tree(root, graph)


def is_bridge(node: PcieNode):
    return node.class_ is not None and node.class_.startswith("0x06")


def get_switch_downstream(node: PcieNode):
    downstream = []

    for child in node.children:
        if is_bridge(child):
            downstream.append(child)

    return downstream


def is_switch(node: PcieNode):
    downstream = get_switch_downstream(node)
    return is_bridge(node) and len(downstream) > 1


def is_multifunction(node: PcieNode):
    return node is not None and node.path.endswith(".x")


def get_multifunction_bridge_bridges(node: PcieNode):
    bridges = []
    for child in node.children:
        if is_bridge(child):
            bridges.append(child)
    return bridges


def get_multifunction_switch_non_bridges(node: PcieNode):
    non_bridges = []
    for child in node.children:
        if not is_bridge(child):
            non_bridges.append(child)
    return non_bridges


def is_multifunction_bridge(node: PcieNode):
    if not is_multifunction(node):
        return False

    bridges = get_multifunction_bridge_bridges(node)
    non_bridges = get_multifunction_switch_non_bridges(node)
    return len(bridges) >= 1 and len(non_bridges) >= 1


def cluster_tree(
    root: PcieNode, graph: Digraph, parent: Optional[PcieNode] = None
) -> None:
    if root is None:
        return

    is_parent_mfb = parent is not None and is_multifunction_bridge(parent)

    if is_multifunction_bridge(root):
        root_id = get_node_id(root)
        mf_cluster_name = f"cluster_mfb_{root_id}"
        with graph.subgraph(name=mf_cluster_name) as mf_cluster:
            mf_cluster.attr(
                cluster="true",
                label="mfb",
                style="filled",
                color="aqua",
                pencolor="black",
            )
            # Add the multifunction root node to the cluster
            mf_cluster.node(get_node_id(root), get_node_label(root))

            bridge = get_multifunction_bridge_bridges(root)[0]
            non_bridges = get_multifunction_switch_non_bridges(root)

            # Add the bridge and non-bridge children to the cluster
            mf_cluster.node(get_node_id(bridge), get_node_label(bridge))
            for nb in non_bridges:
                mf_cluster.node(get_node_id(nb), get_node_label(nb))

            # Add the children of the bridge to the cluster
            for bridge_child in bridge.children:
                mf_cluster.node(get_node_id(bridge_child), get_node_label(bridge_child))

        # Now, continue the clustering process for the grandchildren, but on the main graph
        bridge = get_multifunction_bridge_bridges(root)[0]
        for bridge_child in bridge.children:
            for grandchild in bridge_child.children:
                cluster_tree(grandchild, graph, bridge_child)

        non_bridges = get_multifunction_switch_non_bridges(root)
        for nb in non_bridges:
            for nb_child in nb.children:
                cluster_tree(nb_child, graph, nb)

        return

    # Add the current node to the graph it belongs to
    graph.node(get_node_id(root), label=get_node_label(root))

    if is_switch(root) and not is_parent_mfb:
        cluster_switch(root, graph)
        return

    if is_multifunction(root) and not is_multifunction_bridge(root):
        cluster_multifunction(root, graph)
        return

    # General recursion for children of unclustered nodes
    for child in root.children:
        cluster_tree(child, graph, root)


def cluster_switch(node: PcieNode, graph: Digraph) -> None:
    node_id = get_node_id(node)
    cluster_name = f"cluster_switch_{node_id}"
    with graph.subgraph(name=cluster_name) as cluster:
        cluster.attr(
            cluster="true",
            label="switch",
            style="filled",
            color="lightblue",
            pencolor="black",
        )
        cluster.node(node_id, label=get_node_label(node))

        for child in node.children:
            if is_bridge(child):
                cluster.node(get_node_id(child), get_node_label(child))


def cluster_multifunction(root: PcieNode, graph: Digraph) -> None:
    root_id = get_node_id(root)
    cluster_name = f"cluster_multifunction_{root_id}"
    with graph.subgraph(name=cluster_name) as cluster:
        cluster.attr(
            cluster="true",
            label="multifunction",
            style="filled",
            color="yellow",
            pencolor="black",
        )
        cluster.node(root_id, label=get_node_label(root))

        for child in root.children:
            cluster.node(get_node_id(child), label=get_node_label(child))


def graph_pcie_topology(
    pcie_trees: List[PcieNode],
    filename: str = "pcie_topology",
    format: str = "png",
) -> Digraph:
    graph = Digraph(name="pcie_topology", filename=filename, format=format)
    graph.attr(compound="true")  # Enable edges between clusters

    numa_node_clusters: Dict[Optional[int], List[PcieNode]] = defaultdict(list)
    for root in pcie_trees:
        numa_node = root.numa_node
        if numa_node is not None:
            try:
                numa_node = int(numa_node)
            except (ValueError, TypeError):
                numa_node = -1  # Handle non-integer numa_node values
            numa_node_clusters[numa_node].append(root)

    for numa_node, roots in numa_node_clusters.items():
        name = f"cluster_numa_node_{numa_node}"
        label = f"numa_node_{numa_node}"
        with graph.subgraph(name=name) as numa_cluster:
            numa_cluster.attr(
                cluster="true",
                label=label,
                style="filled",
                color="lightgray",
                pencolor="black",
            )
            for root in roots:
                if root.children:
                    # Omit trees that consist of only a single root.
                    # First, build the visual graph of nodes and edges.
                    graph_tree(root, numa_cluster)
                    # Then, apply the clustering logic in a separate pass.
                    cluster_tree(root, numa_cluster)

    graph.render(filename, view=False, cleanup=True)
    return graph


if __name__ == "__main__":
    pcie_trees = get_pcie_trees("/sys/devices")

    all_roots = []
    # The synthetic node logic needs to be applied carefully.
    # The original implementation had some issues. Let's do a simple pass.
    # A more robust implementation would be needed for complex cases.

    # Let's assume add_synth_multifunction_nodes is run before grouping by NUMA
    processed_trees = []
    for t in pcie_trees:
        add_synth_multifunction_nodes(t)
        processed_trees.append(t)

    graph_pcie_topology(processed_trees)
