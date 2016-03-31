import csv
from db.models import Stop, Route, RouteFrequency, Edge, Base
from digraph import Digraph, DirectedEdge
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

"""
A collection of edges, stops, and routes that make up a transport network.

This replaces the old Network class in Lakbay v1.0.

:Author:     Maded Batara III
:Version:    v2.0 (2016-03-29)
"""

class Network:

    session = None
    engine = None

    def __init__(self, db):
        """
        Creates a transport network interface between the database
        and the algorithm.

        Args:
            db (str): String describing the database location.
        """
        self.db = db

    def __enter__(self):
        """
        Startup commands for the context manager.
        """
        engine = create_engine(self.db)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        edges = self.session.query(Edge)
        self._graph = Digraph(len(edges.all()))
        for edge in edges:
            if not self._graph.has_edge(edge.stop_from_id, edge.stop_to_id):
                self._graph.add_edge(DirectedEdge(
                    edge.stop_from_id, edge.stop_to_id, edge.length
                ))
        return self

    def __exit__(self, type, value, traceback):
        """
        Shutdown commands for the context manager.
        """
        if type is not None:
            pass
        self.session.commit()
        self.session.close()

    @property
    def stops(self):
        """
        List of stops in the transport network. SQLAlchemy query object.
        """
        return self.session.query(Stop)

    @property
    def routes(self):
        """
        List of routes in the transport network. SQLAlchemy query object.
        """
        return session.query(Route)

    @property
    def graph(self):
        """
        Digraph representing the transport network.
        """
        return self._graph

    @property
    def edges(self):
        """
        Edges present in the graph, and routes associated with each edge.
        SQLAlchemy query object.
        """
        return self.session.query(Edge)

    @property
    def route_frequencies(self):
        """
        Frequency tables associated with each route. SQLAlchemy query object.
        """
        return self.session.query(RouteFrequency)
