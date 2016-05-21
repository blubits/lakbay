from db.models import Stop
from dijkstra import shortest_path
from network import Network
from parser import parse_route
from time import perf_counter
from traffic import Traffic

"""
Command-line interface for the Lakbay algorithm.

:Author:     Maded Batara III
:Version:    v3.0 (2015-04-07)
"""

print("Loading databases...")
start_load = perf_counter()
with Network("sqlite:///db/app.db") as network, Traffic(
             "sqlite:///db/traffic.db") as traffic:
    end_load = perf_counter()
    print("Databases loaded, took {0:.2} seconds".format(
        end_load - start_load))

    # Query program
    print("Graph loaded.")
    print()
    src = int(input("Source: "))
    dest = int(input("Destination: "))
    print("Calculating shortest path from '{0}' to '{1}'".format(
        network.stops.filter(Stop.id == src).first().name,
        network.stops.filter(Stop.id == dest).first().name,
    ))

    start_dijk = perf_counter()
    path, time = shortest_path(network.graph, src, dest, [traffic])
    end_dijk = perf_counter()

    print("Dijkstra's took {0:.2} seconds".format(end_dijk - start_dijk))

    start_parse = perf_counter()
    trip = parse_route(path, network, [traffic])
    end_parse = perf_counter()

    print("parse_route() took {0:.2} seconds".format(end_parse - start_parse))
    print()
    print(trip)
    print()
