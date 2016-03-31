from sqlalchemy import Boolean, Column, Integer, String, Float, Time, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

"""
Models for the Network class.

This is a replacement of a bulk of the functionality present in the transport
network classes in Lakbay v1.0.

:Author:     Maded Batara III
:Version:    v1.0 (2016-03-24)
"""

Base = declarative_base()

class Stop(Base):
    __tablename__ = "stops"

    id = Column(Integer, primary_key=True)
    stop_id = Column(String, index=True, unique=True)
    name = Column(String)
    lat = Column(Float)
    long = Column(Float)

    def __init__(self, name, lat, long, stop_id):
        """
        Constructs a transport network stop.

        Args:
            name (str): Name of the stop. Column "stop_name" in
                gtfs/routes.txt.
            lat (float): Latitude of the stop. Column "stop_lat" in
                gtfs/routes.txt.
            long (float): Longitude of the stop. Column "stop_lon" in
                gtfs_routes.txt.
            stop_id (str): Stop ID. Column "stop_id" in gtfs_routes.txt.
        """
        self.name = name
        self.lat = lat
        self.long = long
        self.stop_id = stop_id

    def __repr__(self):
        """
        Returns repr(self).
        """
        return "<Stop {0} ({1}, {2})>".format(self.name, self.lat, self.long)

class Route(Base):
    __tablename__ = "routes"

    id = Column(Integer, primary_key=True)
    trip_id = Column(String, index=True, unique=True)
    route_id = Column(String, index=True)
    service_id = Column(String, index=True)
    name = Column(String)
    description = Column(String)

    frequency = relationship("RouteFrequency", uselist=False,
        back_populates="route")

    def __init__(self, name, description, trip_id, route_id, service_id):
        """
        Constructs a transport network route.

        Args:
            name (str): Name of the route. Column "route_long_name" in
                gtfs/routes.txt.
            description (str): Route description. Column "route_description"
                in gtfs/routes.txt.
            trip_id (str): Trip ID. Column "trip_id" in gtfs/trips.txt.
            route_id (str): Route ID. Column "route_id" in gtfs/trips.txt.
            service_id (str): Service ID. Column "service_id" in
                gtfs/trips.txt.
        """
        self.name = name
        self.description = description
        self.trip_id = trip_id
        self.route_id = route_id
        self.service_id = service_id

    def __repr__(self):
        """
        Returns repr(self).
        """
        return "<Route {0} ({1}/{2})>".format(
            self.id, self.route_id, self.trip_id)

class Edge(Base):
    __tablename__ = "graph"

    id = Column(Integer, primary_key=True)
    stop_from_id = Column(Integer, ForeignKey("stops.id"))
    stop_to_id = Column(Integer, ForeignKey("stops.id"))
    route_id = Column(Integer, ForeignKey("routes.id"))
    sequence_id = Column(Integer)
    length = Column(Integer)

    stop_to = relationship("Stop", foreign_keys=[stop_to_id], uselist=False)
    stop_from = relationship("Stop", foreign_keys=[stop_from_id], uselist=False)
    route = relationship("Route", uselist=False)

    def __init__(self, stop_from, stop_to, route, sequence_id, length):
        """
        Constructs an edge in the transport network graph.

        Args:
            stop_from (Stop): Origin stop of edge.
            stop_to (Stop): Destination stop of edge.
            route (Route): Route associated with edge.
            sequence_id (int): Sequence ID.
            length (int): Length of edge.
        """
        self.stop_from = stop_from
        self.stop_to = stop_to
        self.route = route
        self.sequence_id = sequence_id
        self.length = length

    def __repr__(self):
        return "<Edge {0}->{1} ({2}), length {3}>".format(
            self.stop_to_id, self.stop_from_id, self.route_id, self.length)

class RouteFrequency(Base):
    __tablename__ = "frequencies"

    id = Column(Integer, ForeignKey('routes.id'),
        index=True, primary_key=True)
    start = Column(Time)
    end = Column(Time)
    headway = Column(Integer)
    mon = Column(Boolean)
    tue = Column(Boolean)
    wed = Column(Boolean)
    thu = Column(Boolean)
    fri = Column(Boolean)
    sat = Column(Boolean)
    sun = Column(Boolean)

    route = relationship("Route", back_populates="frequency")

    def __init__(self, start, end, headway,
        mon, tue, wed, thu, fri, sat, sun):
        """
        Constructs a frequency table for a transport network route.

        Args:
            start (datetime.time): Time when the route's service starts.
                Column "start_time" in gtfs/frequencies.txt.
            end (datetime.time): Time when the route's service stops.
                Column "end_time" in gtfs/frequencies.txt.
            headway (int): Approximate time between arrivals, in seconds.
                Column "headway_secs" in gtfs/frequencies.txt.
            mon (bool), tue (bool), wed (bool), thu (bool), fri (bool),
            sat (bool), sun (bool): Whether the route is available
                that day. Columns "monday" to "sunday" in gtfs/calendar.txt.
        """
        self.start = start
        self.end = end
        self.headway = headway
        self.mon = mon
        self.tue = tue
        self.wed = wed
        self.thu = thu
        self.fri = fri
        self.sat = sat
        self.sun = sun

    def __repr__(self):
        """
        Returns repr(self).
        """
        return "<RouteFrequency {0} (<Route {1}>)>".format(
            self.id, self.route_id)


