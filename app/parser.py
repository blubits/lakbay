from db.models import Edge
from digraph import DirectedEdge
from trip import Trip

"""
Parses a set of routes and converts it to a
human-readable trip format.

:Author:     Maded Batara III
:Version:    v2.0dev (2015-12-25)
"""

# Threshold for the algorithm to consider walking instead of riding
WALKING_THRESHOLD = 150     # 2.5 minutes

# Walking route ID
WALKING_ROUTE_ID = 1865

def path_length(vertex_list, modifiers):
    """
    Gets the modified (with weight multipliers) length of a path on the graph.

    Assumes the graph is not a multigraph.

    Args:
        vertex_list (list(Edge)): A list of edges that constitute the part
            of the route.
        modifiers (list): List of weight modifiers, see djikstra.weight().

    Returns:
        The total length of the path, if the path exists.
    """
    length = 0
    for edge in vertex_list:
        fr, to = edge.stop_from_id, edge.stop_to_id
        edge_length = edge.length
        for modifier in modifiers:
            edge_length *= modifier.get_multiplier(
                DirectedEdge(fr, to, edge_length)
            )
        length += edge_length
    return length

def parse_route(stop_list, network, modifiers):
    """
    From the output by Dijkstra's algorithm (dijkstra.py),
    output a list of routes (trip) a person can take.

    Args:
        stop_list (list): A list of integers, representing the shortest
            path from two nodes.
        network (Network): The transport network to use as a data
            source.
        modifiers (list): List of weight modifiers, see djikstra.weight().

    Returns:
        A Trip object containing the list of routes to be taken constituting
        the path, in the following format:
            [{
                "from": (int),
                "to": (int),
                "route_id": (str),
                "travel_time": (int)
            }..]
    """
    start = stop_list[0]
    end = stop_list[-1]

    # Get all routes that pass by each edge of the stop list
    route_counter = {}
    for i in range(len(stop_list) - 1):
        fr, to = stop_list[i], stop_list[i + 1]
        edges = network.edges.filter(
            Edge.stop_from_id == fr, Edge.stop_to_id == to)
        for edge in edges:
            route_id = edge.route_id
            if route_id not in route_counter:
                route_counter[route_id] = [1, (fr, to)]
            else:
                route_counter[route_id][0] += 1
                route_counter[route_id].append((fr, to))

    # Get the length of each route
    route_spans = {node: [] for node in stop_list}
    for route_id, route in route_counter.items():
        length = route[0]
        route_end = route[-1][1]
        edges = route[1:]
        for edge in edges:
            curr_start = edge[0]
            route_spans[curr_start].append((
                length, route_id, route_end
            ))
            length -= 1

    curr_node = start
    path = []

    # Heuristic algorithm for getting the next route:
    # 1. Get top 10% routes at the current node
    # 2. For each route, get the node where it goes to:
    #    calculate a heuristic measure (average length of
    #    routes at that node? total number of unique routes
    #    at that node? both?)
    # 3. The route with the best heuristic measure will
    #    be chosen, current node will be moved, algorithm repeats
    while curr_node != end:
        possible_routes = route_spans[curr_node]
        next_stops = set()
        for route in possible_routes:
            next_stops.add(route[2])
        # Determine where to stop
        max_heuristic = float("-inf")
        max_stop = ""
        for stop in next_stops:
            curr_heuristic = density_heuristic(
                curr_node, stop, stop_list, route_spans
            )
            if max_heuristic < curr_heuristic:
                max_heuristic = curr_heuristic
                max_stop = stop
        # Determine what route to take
        max_route = ()
        for route in possible_routes:
            if route[2] == max_stop:
                max_route = (curr_node, *route)
        path.append(max_route)
        curr_node = max_stop

    # Process path list and return
    parsed_path = []
    for fr, _, route_id, to in path:
        start = network.edges.filter(
            Edge.route_id == route_id,
            Edge.stop_from_id == fr).first().sequence_id
        end = network.edges.filter(
            Edge.route_id == route_id,
            Edge.stop_to_id == to).first().sequence_id
        route_edges = network.edges.filter(
            Edge.route_id == route_id, Edge.sequence_id >= start,
            Edge.sequence_id <= end).all()
        travel_time = path_length(route_edges, modifiers)
        route = {
            "from": fr,
            "to": to,
            "route_id": WALKING_ROUTE_ID if travel_time <= WALKING_THRESHOLD
            else route_id,
            "travel_time": travel_time
        }
        # If route is walking, get the route it tried to replace
        # and put it in the modified_route_id attribute for parsers
        # to use if they want to get the path.
        # if route["route_id"] == WALKING_ROUTE_ID:
        #    route["modified_route_id"] = route_id
        parsed_path.append(route)

    return Trip(network, parsed_path)

def density_heuristic(current_stop, heuristic_stop, stop_list, route_spans):
    """
    Calculates the density heuristic for a certain stop, based on the
    following properties:
        (1) The number of routes at that stop.
        (2) The average length of a route that starts at that stop.
        (3) Distance from the initial stop.
    """
    # (1) The number of routes at that stop
    len_routes = len(route_spans[heuristic_stop])
    # (2) The average length of a route that starts at that stop
    ave_len_route = 0
    for route in route_spans[heuristic_stop]:
        ave_len_route += route[0]
    try:
        ave_len_route /= len_routes
    except ZeroDivisionError:
        ave_len_route = 1
        len_routes = 1
    # (3) Distance from the initial stop
    dist_stop = stop_list.index(heuristic_stop) - stop_list.index(current_stop)
    # print("{0}: heuristic {1} ({3}|{4})".format(
    #     heuristic_stop, ave_len_route * dist_stop,
    #     len_routes, ave_len_route, dist_stop
    # ))
    return ave_len_route * dist_stop
