from db.traffic_constants import WEIGHTS
from db.traffic_models import Base, EdgeTraffic, TrafficSituation
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

"""
Python wrapper for the trapik.acacialabs.com/MMDA/InterAksyon
live traffic feed.

:Author:     Maded Batara III
:Version:    v2.0 (2016-03-29)
"""

class Traffic:

    def __init__(self, db):
        """
        Creates a traffic feed interface between the database
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
        edge_traffic = self.session.query(EdgeTraffic)
        self.edges = {}
        for edge in edge_traffic:
            self.edges[
                (edge.stop_from_id, edge.stop_to_id)
            ] = edge.traffic.status
        return self

    def __exit__(self, type, value, traceback):
        """
        Shutdown commands for the context manager.
        """
        if type is not None:
            pass
        self.session.commit()
        self.session.close()

    def get_multiplier(self, edge):
        """
        Gets the edge multiplier as determined by the traffic situation.

        Args:
            edge (DirectedEdge): Edge to get multiplier for.
        """
        edge_tuple = (edge.vertex_from, edge.vertex_to)
        try:
            return WEIGHTS[self.edges[edge_tuple]]
        except KeyError:
            return 1    # No change

