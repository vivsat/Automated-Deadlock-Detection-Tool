def parse_input_data(logs):
    """
    Parse input logs and extract process-resource relationships.
    Input format: List of strings, e.g., ["P1 -> R1", "P2 -> R2", "R1 -> P2"]
    """
    edges = []
    for log in logs:
        parts = log.split("->")
        if len(parts) == 2:
            edges.append((parts[0].strip(), parts[1].strip()))
    return edges


def build_resource_allocation_graph(edges):
    """
    Build a directed graph from the parsed edges.
    """
    graph = nx.DiGraph()
    graph.add_edges_from(edges)
    return graph
