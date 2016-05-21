from heapq import heappop, heapify

"""
Looks for a shortest path between two nodes in a weighted graph
using Dijkstra's algorithm.

:Author:     Maded Batara III
:Version:    v8.0 (2016-04-01)
"""

def shortest_path(graph, src, dest, modifiers):
    """
    Computes the shortest possible path from a source vertex to a destination
    vertex in a graph.

    Args:
        graph (Digraph): Graph to operate on.
        src (int): Source vertex.
        dest (int): Destination vertex.
        modifiers (list): List of weight modifiers, see weight().

    Note:
        As the number of edges in the graph grows, the performance of
        this algorithm will decrease, so this algorithm best performs
        on sparse graphs.

    Returns:
        A list [src, a, b, ..., dest] such that src -> a -> b -> ... -> dest
        is the shortest possible path from src to dest in the graph.
    """
    # Distances to source node
    distances = {vertex: float("inf") for vertex in range(graph.num_vertices)}
    # Previous node in optimal path
    previous = {vertex: -1 for vertex in range(graph.num_vertices)}
    # Shortest path from source to source is 0
    distances[src] = 0
    # Initialize priority queue and vertex set
    pqueue = [(distances[src], src)]
    vertex_set = {src}

    while len(pqueue) != 0:
        vertex_added = False
        curr = heappop(pqueue)[1]
        vertex_set.remove(curr)
        for neighbor in graph.outgoing(curr):
            alt = distances[curr] + weight(neighbor, modifiers)
            other = neighbor.other(curr)    # Opposite vertex
            if alt < distances[other]:
                distances[other] = alt
                previous[other] = curr
                if other not in vertex_set:
                    vertex_added = True
                    pqueue.append((alt, other))
                    vertex_set.add(other)
        if vertex_added:
            heapify(pqueue)

    # Shortest path
    shortest_path = []
    shortest_path_distance = distances[dest]

    # Traverse previous[] to look for shortest path to target
    current_node = dest
    while previous[current_node] != -1:
        shortest_path.append(current_node)
        current_node = previous[current_node]
    if len(shortest_path) != 0:
        shortest_path.append(current_node)
        shortest_path.reverse()

    return shortest_path, shortest_path_distance

def weight(edge, modifiers):
    """
    Gets the modified weight of the edge.

    Args:
        edge (DirectedEdge): Edge to get weight from.
        modifiers (list): A list of objects that modify the edge weight.
            These objects must support get_multiplier(edge).
    """
    weight = edge.weight
    for modifier in modifiers:
        weight *= modifier.get_multiplier(edge)
    return weight
