import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

import datetime
import requests
from network import Network
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from traffic_constants import PLACES, TRAFFIC_ROOT
from traffic_models import Base, EdgeTraffic, TrafficSituation

"""
Database creator for the Traffic class.

:Author:     Maded Batara III
:Version:    v1.0 (2016-03-29)
"""

# Create database
engine = create_engine('sqlite:///traffic.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Helper functions
def parse_places(places, graph):
    """
    Parses the PLACES constant for easier querying by the Traffic object.

    Args:
        places (dict): PLACES constant, see constants.py.
        graph (Digraph): Transport network of nodes.
    """
    edge_list = {}
    for node_list, place in places.items():
        place_nb = (place[0], place[1] + 1, "north_bound")
        place_sb = (place[0], place[1] + 1, "south_bound")
        # Southbound paths
        edges = generate_edges(node_list)
        for edge in edges:
            if graph.has_edge(*edge):
                edge_list[edge] = place_sb
        # Northbound paths
        rev_edges = generate_edges(tuple(reversed(node_list)))
        for edge in rev_edges:
            if graph.has_edge(*edge):
                edge_list[edge] = place_nb
        # Corner edges are edges with exactly one vertex along the path.
        for node in node_list:
            # Southbound corner edge: (node, x) -> use graph.outgoing()
            for edge in graph.outgoing(node):
                edge_tuple = (edge.vertex_from, edge.vertex_to)
                if edge_tuple not in edge_list:
                    edge_list[edge_tuple] = place_sb
            # Northbound corner edge: (x, node) -> use graph.incoming()
            for edge in graph.incoming(node):
                edge_tuple = (edge.vertex_from, edge.vertex_to)
                if edge_tuple not in edge_list:
                    edge_list[edge_tuple] = place_nb
    return edge_list

def generate_edges(node_list):
    """
    From a list of nodes, generate a list of directed edges, where
    every node points to a node succeeding it in the list.

    As the PLACES variable is 0-based, the algorithm also adapts it
    to the 1-based system v2.0 uses.

    Argss:
        node_list (list(int)): List of nodes.
    """
    edges = []
    for i in range(len(node_list)):
        for j in range(i + 1, len(node_list)):
            edges.append((node_list[i] + 1, node_list[j] + 1))
    return edges

# TABLE traffic
traffic_table = []
for i in range(1, 11):
    try:
        traffic_file = requests.get("{0}/{1}/".format(TRAFFIC_ROOT, i))
        traffic_file.encoding = "utf-8-sig"
        traffic_json = traffic_file.json()
        for line in traffic_json["lines"]:
            for direction, situation in line["status"].items():
                traffic_table.append(TrafficSituation(
                    traffic_json["area"]["area_id"],
                    line["line_order"],
                    direction,
                    situation["status"],
                    datetime.datetime.strptime(
                        line["last_updated"], '%I:%M %p').time()
                ))
    except (ConnectionResetError, requests.exceptions.ConnectionError):
        raise RuntimeError("Can't connect to {0}/{1}/, check your "
                           "internet connection?".format(
                               TRAFFIC_ROOT, i))
session.add_all(traffic_table)

# TABLE edges
edges_table = []
with Network("sqlite:///app.db") as network:
    for edge, traffic in parse_places(PLACES, network.graph).items():
        for row in session.query(TrafficSituation).filter(
                   TrafficSituation.area_id == int(traffic[0]),
                   TrafficSituation.line_id == int(traffic[1]),
                   TrafficSituation.direction == traffic[2]):
            edges_table.append(EdgeTraffic(int(edge[0]), int(edge[1]), row))
session.add_all(edges_table)

session.commit()
session.close()
