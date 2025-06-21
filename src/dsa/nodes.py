from typing import Any, NewType
import networkx as nx


# derived from https://github.com/langflow-ai/langflow/pull/5261
def find_last_node(nodes, edges):
    """This function receives a flow and returns the last node."""
    source_ids = {e["source"] for e in edges}
    for n in nodes:
        if n["id"] not in source_ids:
            return n
    return None


# Function to find all leaf nodes (nodes with no outgoing edges)
def find_leaf_nodes(nodes: list[dict], edges: list[dict]) -> list[dict]:
    leaf_nodes = []
    for node in nodes:
        is_leaf = True
        for edge in edges:
            if edge["source"] == node["id"]:
                is_leaf = False
                break
        if is_leaf:
            leaf_nodes.append(node)
    return leaf_nodes


JsonRef = NewType("JsonRef", str)


# derived from https://github.com/pydantic/pydantic/pull/9650
def _get_all_json_refs(item: Any) -> set[JsonRef]:
    """Get all the definitions references from a JSON schema."""
    refs: set[JsonRef] = set()
    if isinstance(item, dict):
        for key, value in item.items():
            if key == "$ref" and isinstance(value, str):
                # the isinstance check ensures that '$ref' isn't the name of a property, etc.
                refs.add(JsonRef(value))
            elif isinstance(value, dict):
                refs.update(_get_all_json_refs(value))
            elif isinstance(value, list):
                for item in value:
                    refs.update(_get_all_json_refs(item))
    elif isinstance(item, list):
        for item in item:
            refs.update(_get_all_json_refs(item))
    return refs


# derived from https://github.com/langflow-ai/langflow/pull/5262
def find_cycle_vertices(edges):
    # Create a directed graph from the edges
    graph = nx.DiGraph(edges)

    # Find all simple cycles in the graph
    cycles = list(nx.simple_cycles(graph))

    # Flatten the list of cycles and remove duplicates
    cycle_vertices = {vertex for cycle in cycles for vertex in cycle}

    return sorted(cycle_vertices)


# derived from https://github.com/langflow-ai/langflow/pull/5263
def sort_chat_inputs_first(self, vertices_layers: list[list[str]]) -> list[list[str]]:
    # First check if any chat inputs have dependencies
    for layer in vertices_layers:
        for vertex_id in layer:
            if "ChatInput" in vertex_id and self.get_predecessors(
                self.get_vertex(vertex_id)
            ):
                return vertices_layers

    # If no chat inputs have dependencies, move them to first layer
    chat_inputs_first = []
    for layer in vertices_layers:
        layer_chat_inputs_first = [
            vertex_id for vertex_id in layer if "ChatInput" in vertex_id
        ]
        chat_inputs_first.extend(layer_chat_inputs_first)
        for vertex_id in layer_chat_inputs_first:
            # Remove the ChatInput from the layer
            layer.remove(vertex_id)

    if not chat_inputs_first:
        return vertices_layers

    return [chat_inputs_first, *vertices_layers]


# Function to find the node with highest degree (most connections)
def find_node_with_highest_degree(
    nodes: list[str], connections: dict[str, list[str]]
) -> str:
    max_degree = -1
    max_degree_node = None

    for node in nodes:
        degree = 0
        # Count outgoing connections
        degree += len(connections.get(node, []))

        # Count incoming connections
        for src, targets in connections.items():
            if node in targets:
                degree += 1

        if degree > max_degree:
            max_degree = degree
            max_degree_node = node

    return max_degree_node


def find_node_clusters(nodes: list[dict], edges: list[dict]) -> list[list[dict]]:
    # Create node ID to node mapping for easy lookup
    node_map = {node["id"]: node for node in nodes}

    # Create an adjacency list
    adjacency = {}
    for edge in edges:
        src = edge["source"]
        tgt = edge["target"]

        if src not in adjacency:
            adjacency[src] = []
        if tgt not in adjacency:
            adjacency[tgt] = []

        adjacency[src].append(tgt)
        adjacency[tgt].append(src)  # Assuming undirected graph for clustering

    # Track visited nodes
    visited = set()
    clusters = []

    for node in nodes:
        node_id = node["id"]
        if node_id in visited:
            continue

        # Start a new cluster
        cluster = []
        queue = [node_id]
        visited.add(node_id)

        while queue:
            current = queue.pop(0)
            cluster.append(node_map[current])

            for neighbor in adjacency.get(current, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        clusters.append(cluster)

    return clusters


def calculate_node_betweenness(
    nodes: list[str], edges: list[dict[str, str]]
) -> dict[str, float]:
    betweenness = {node: 0.0 for node in nodes}

    # For each pair of nodes, find all shortest paths and count paths through each node
    for source in nodes:
        for target in nodes:
            if source == target:
                continue

            # Find all shortest paths from source to target
            all_paths = []

            # BFS to find shortest path length
            queue = [(source, [source])]
            shortest_length = float("inf")

            while queue:
                current, path = queue.pop(0)

                # If we've found a path to target
                if current == target:
                    all_paths.append(path)
                    continue

                if len(path) > shortest_length:
                    continue

                for edge in edges:
                    if edge["source"] == current and edge["target"] not in path:
                        new_path = path + [edge["target"]]
                        queue.append((edge["target"], new_path))

                        if edge["target"] == target:
                            shortest_length = len(new_path) - 1

            # Count how many shortest paths go through each node
            for path in all_paths:
                for node in path[1:-1]:  # Exclude source and target
                    betweenness[node] += 1.0 / len(all_paths)

    return betweenness


def find_strongly_connected_components(
    nodes: list[str], edges: list[dict[str, str]]
) -> list[list[str]]:
    # Build adjacency list
    graph = {}
    for node in nodes:
        graph[node] = []

    for edge in edges:
        src = edge["source"]
        tgt = edge["target"]
        if src in graph:
            graph[src].append(tgt)

    # Find SCCs using a simplified version of Kosaraju's algorithm
    visited = set()
    stack = []

    # First DFS to fill the stack
    def fill_order(node):
        visited.add(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                fill_order(neighbor)
        stack.append(node)

    for node in nodes:
        if node not in visited:
            fill_order(node)

    # Create reversed graph
    reversed_graph = {}
    for node in nodes:
        reversed_graph[node] = []

    for edge in edges:
        src = edge["source"]
        tgt = edge["target"]
        if tgt in reversed_graph:
            reversed_graph[tgt].append(src)

    # Second DFS to find SCCs
    visited = set()
    sccs = []

    def collect_scc(node, component):
        visited.add(node)
        component.append(node)
        for neighbor in reversed_graph.get(node, []):
            if neighbor not in visited:
                collect_scc(neighbor, component)

    while stack:
        node = stack.pop()
        if node not in visited:
            component = []
            collect_scc(node, component)
            sccs.append(component)

    return sccs
