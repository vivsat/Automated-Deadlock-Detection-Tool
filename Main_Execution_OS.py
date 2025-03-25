import networkx as nx
import matplotlib.pyplot as plt

# ======================
# Data Processing Module
# ======================

def parse_input_data(logs):
    #Give input in form of list as P1->R1
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


# ======================
# Deadlock Detection Module
# ======================

def detect_deadlock(graph):

    #Detect deadlock by finding cycles in RAG.

    try:
        cycle = nx.find_cycle(graph, orientation="original")
        return True, cycle
    except nx.NetworkXNoCycle:
        return False, None


def suggest_resolution(cycle):
    # Giving Suggestions
    if cycle:
        resolution = f"Terminate one of the processes in the cycle: {cycle}"
        return resolution
    return "No deadlock detected."


def preempt_resource(graph, cycle):
    
    # Break the deadlock by preempting a reaource from one process in the cycle.
    if not cycle:
        return graph, "No deadlock to resolve."

    # Select the first edge in the cycle to preempt
    preempt_edge = cycle[0]
    process, resource = preempt_edge[0], preempt_edge[1]

    # Remove the edge from the graph
    graph.remove_edge(process, resource)

    return graph, f"Preempted resource {resource} from process {process}."


# ======================
# Visualization Module
# ======================

def visualize_graph(graph, deadlock_cycle=None):
   
    #Visualize the RAG with deadlock
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


# ======================
# Main Execution
# ======================

def get_user_input():
    #getting input from user
    
    logs = []
    print("Enter process-resource relationships (e.g., 'P1 -> R1'). Type 'done' to finish.")
    while True:
        user_input = input("Enter relationship: ").strip()
        if user_input.lower() == "done":
            break
        logs.append(user_input)
    return logs


def main():
    # Step 1: Get user input
    logs = get_user_input()

    # Step 2: Data Processing
    edges = parse_input_data(logs)
    graph = build_resource_allocation_graph(edges)

    # Step 3: Deadlock Detection
    deadlock_detected, deadlock_cycle = detect_deadlock(graph)
    if deadlock_detected:
        print("\nDeadlock Detected!")
        print("Deadlock Cycle:", deadlock_cycle)
        resolution = suggest_resolution(deadlock_cycle)
        print("Resolution Suggestion:", resolution)
    else:
        print("\nNo Deadlock Detected.")

    # Step 4: Visualization
    visualize_graph(graph, deadlock_cycle)

    # Step 5: Preempt Resource (Optional)
    if deadlock_detected:
        preempt = input("\nDo you want to preempt a resource to resolve the deadlock? (yes/no): ").strip().lower()
        if preempt == "yes":
            graph, resolution = preempt_resource(graph, deadlock_cycle)
            print(resolution)

            # Re-detect deadlock after preemption
            deadlock_detected, deadlock_cycle = detect_deadlock(graph)
            if deadlock_detected:
                print("Deadlock still exists!")
            else:
                print("Deadlock resolved!")

            # Update visualization
            visualize_graph(graph, deadlock_cycle)


if __name__ == "__main__":
    main()
