from sqlalchemy import Column, Integer, String, Time, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

"""
Models and constants for the Traffic class.

:Author:     Maded Batara III
:Version:    v1.0 (2016-03-29)
"""

Base = declarative_base()

class TrafficSituation(Base):
    __tablename__ = "traffic"

    id = Column(Integer, primary_key=True)
    area_id = Column(Integer, index=True)
    line_id = Column(Integer, index=True)
    direction = Column(String, index=True)
    status = Column(String)
    updated_time = Column(Time)

    def __init__(self, area_id, line_id, direction, status, updated_time):
        """
        Constructs a new traffic situation description along an area.

        Args:
            area_id (int): Area ID. "area" > "area_id" in JSON.
            line_id (int): Line ID within the area. "lines" > "line_order"
                in JSON.
            direction (str): Direction of cars in the area, either "north_bound"
                or "south_bound".
            status (str): Density of traffic in the area.
            updated_time (datetime.time): Time of information's last update.
        """
        self.area_id = area_id
        self.line_id = line_id
        self.direction = direction
        self.status = status
        self.updated_time = updated_time

    def __repr__(self):
        """
        Returns repr(self).
        """
        return "<TrafficSituation {0}|{1}|{2}>".format(
            self.area_id, self.line_id, self.direction)

class EdgeTraffic(Base):
    __tablename__ = "edges"

    id = Column(Integer, primary_key=True)
    stop_from_id = Column(Integer)
    stop_to_id = Column(Integer)
    traffic_id = Column(Integer, ForeignKey("traffic.id"))

    traffic = relationship("TrafficSituation", uselist=False)

    def __init__(self, stop_from_id, stop_to_id, traffic):
        """
        Creates an association between an edge and the traffic along that edge.

        Args:
            stop_from_id (int): Origin stop of edge.
            stop_to_id (int): Destination stop of edge.
            traffic (TrafficSituation): Traffic situation along that edge.
        """
        self.stop_from_id = stop_from_id
        self.stop_to_id = stop_to_id
        self.traffic = traffic

    def __repr__(self):
        """
        Returns repr(self).
        """
        return "<EdgeTraffic {0}->{1} ({2})>".format(
            self.stop_from_id, self.stop_to_id, self.traffic)