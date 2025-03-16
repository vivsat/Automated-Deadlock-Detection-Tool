def detect_deadlock(graph):
    """
    Detect deadlock by finding cycles in the resource allocation graph.
    """
    try:
        cycle = nx.find_cycle(graph, orientation="original")
        return True, cycle
    except nx.NetworkXNoCycle:
        return False, None


def suggest_resolution(cycle):
    """
    Suggest a resolution for the detected deadlock.
    """
    if cycle:
        resolution = f"Terminate one of the processes in the cycle: {cycle}"
        return resolution
    return "No deadlock detected."


def preempt_resource(graph, cycle):
    """
    Break the deadlock by preempting a resource from one of the processes in the cycle.
    """
    if not cycle:
        return graph, "No deadlock to resolve."

    # Select the first edge in the cycle to preempt
    preempt_edge = cycle[0]
    process, resource = preempt_edge[0], preempt_edge[1]

    # Remove the edge from the graph
    graph.remove_edge(process, resource)

    return graph, f"Preempted resource {resource} from process {process}."
