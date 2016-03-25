from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

"""
Models for the Network class.

This is a replacement of a bulk of the functionality present in the transport
network classes in Lakbay v1.0.

:Author:     Maded Batara III
:Version:    v1.0dev (2016-03-24)
"""

Base = declarative_base()

class Stop(Base):
    __tablename__ = "stops"

    id = Column(Integer, primary_key=True, index=True)
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
        return "<Stop {0} ({1}, {2})>".format(name, lat, lng)

class Route(Base):
    __tablename__ = "routes"

    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(String, index=True, unique=True)
    route_id = Column(String, index=True)
    name = Column(String)
    description = Column(String)

    def __init__(self, name, description, trip_id, route_id):
        """
        Constructs a transport network route.

        Args:
            name (str): Name of the route. Column "route_long_name" in
                gtfs/routes.txt.
            description (str): Route description. Column "route_description"
                in gtfs/routes.txt.
            trip_id (str): Trip ID. Column "trip_id" in gtfs/trips.txt.
            route_id (str): Route ID. Column "route_id" in gtfs/trips.txt.
        """
        self.name = name
        self.description = description
        self.trip_id = trip_id
        self.route_id = route_id

    def __repr__(self):
        """
        Returns repr(self).
        """
        return "<Route {0} ({1}/{2})>".format(id, route_id, trip_id)

#class RouteFrequency(Base):
#    __tablename__ = "frequencies"

#class RouteStops(Base):
#    __tablename__ = "route_stops"