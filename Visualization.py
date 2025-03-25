def visualize_graph(graph, deadlock_cycle=None):
    """
    Visualize the resource allocation graph with deadlock cycle highlighted.
    """
    pos = nx.spring_layout(graph)
    plt.figure(figsize=(8, 6))

    # Draw nodes and edges
    nx.draw_networkx_nodes(graph, pos, node_size=2000, node_color="lightblue")
    nx.draw_networkx_edges(graph, pos, edge_color="gray", arrowstyle="->", arrowsize=20)
    nx.draw_networkx_labels(graph, pos, font_size=12, font_weight="bold")

    # Highlight deadlock cycle
    if deadlock_cycle:
        cycle_edges = [(u, v) for u, v, _ in deadlock_cycle]
        nx.draw_networkx_edges(graph, pos, edgelist=cycle_edges, edge_color="red", arrowstyle="->", arrowsize=20)

    plt.title("Resource Allocation Graph")
    plt.show()
