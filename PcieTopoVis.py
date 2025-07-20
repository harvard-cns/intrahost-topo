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
    for n in root.children:
        if n is node:
            return root
        parent = get_node_parent(n, node)
        if parent:
            return parent
    return None


def get_node_siblings(root: PcieNode, node: PcieNode) -> Optional[List[PcieNode]]:
    parent = get_node_parent(root, node)
    if parent is None:
        return None
    return parent.children


def get_same_device_siblings(root: PcieNode, node: PcieNode) -> List[PcieNode]:
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


def graph_tree(root: PcieNode, curr_node: PcieNode, graph: Digraph) -> None:
    curr_node_id = get_node_id(curr_node)
    curr_node_label = get_node_label(curr_node)

    if curr_node.class_ and curr_node.class_.startswith("0x06"):
        cluster = Digraph(name=f"cluster_{curr_node_id}")
        cluster.attr(
            cluster="true",
            label=f"bridge_{curr_node.class_}",
            style="filled",
            color="lightblue",
            pencolor="black",
        )

        cluster.node(curr_node_id, label=curr_node_label)
        for child in curr_node.children:
            child_id = get_node_id(child)
            child_label = get_node_label(child)
            cluster.node(child_id, label=child_label)
            cluster.edge(curr_node_id, child_id)
            graph_tree(root, child, cluster)

        graph.subgraph(cluster)

    elif "x" in curr_node.path:
        # `curr_node` is a synthetic multifunction node.
        cluster = Digraph(name=curr_node.path)
        cluster.attr(
            cluster="true",
            label=f"multifunction_{curr_node.path}",
            style="filled",
            color="yellow",
            pencolor="black",
        )

        cluster.node(curr_node_id, label=curr_node_label)
        for child in curr_node.children:
            child_id = get_node_id(child)
            child_label = get_node_label(child)
            cluster.node(child_id, label=child_label)
            cluster.edge(curr_node_id, child_id)
            graph_tree(root, child, cluster)

        graph.subgraph(cluster)

    else:
        graph.node(curr_node_id, label=curr_node_label)
        for child in curr_node.children:
            graph.node(get_node_id(child), label=get_node_label(child))
            graph.edge(curr_node_id, get_node_id(child))
            graph_tree(root, child, graph)


def graph_pcie_topology(
    pcie_trees: List[PcieNode],
    filename: str = "pcie_topology",
    format: str = "png",
) -> Digraph:
    graph = Digraph(name="pcie_topology", filename=filename, format=format)

    numa_node_clusters: Dict[Optional[int], List[PcieNode]] = defaultdict(list)
    for root in pcie_trees:
        numa_node = root.numa_node
        if numa_node is not None:
            numa_node = int(numa_node)
            numa_node_clusters[numa_node].append(root)

    for numa_node, cluster in numa_node_clusters.items():
        name = f"numa_node_{numa_node}"
        label = f"numa_node_{numa_node}"
        numa_cluster = Digraph(name=name)
        numa_cluster.attr(
            cluster="true",
            label=label,
            style="filled",
            color="lightgray",
            pencolor="black",
        )
        for root in cluster:
            if root.children:
                # Omit trees that consist of only the root.
                graph_tree(root, root, numa_cluster)
        graph.subgraph(numa_cluster)

    graph.render(filename)
    return graph


def add_synth_multifunction_nodes(root: PcieNode) -> None:
    if root is None:
        return
    if root.children == []:
        return

    for child in root.children:
        same_device_siblings = get_same_device_siblings(root, child)
        if len(same_device_siblings) > 1:
            # Remove `same_device_siblings` from `root.children`.
            for sd_sibling in same_device_siblings:
                # Remove `sd_sibling` from `root.children`.
                for c in root.children:
                    if c.path == sd_sibling.path:
                        root.children.remove(c)
            prefix = basename(child.path)[:-1]
            synth_multifunction_node = PcieNode(f"{prefix}x")
            synth_multifunction_node.children = same_device_siblings
            root.children.append(synth_multifunction_node)


if __name__ == "__main__":
    pcie_trees = get_pcie_trees("/sys/devices")
    # Omit trees that consist of only the root.
    for t in pcie_trees:
        if t.children == []:
            pcie_trees.remove(t)

    for t in pcie_trees:
        add_synth_multifunction_nodes(t)

    graph_pcie_topology(pcie_trees)
