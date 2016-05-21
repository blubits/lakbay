import csv
import datetime
from models import Stop, Route, RouteFrequency, Edge, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

"""
Database creator from the GTFS class.

As this is a database creator, should only be executed when there is an
update in the underlying data source. The existing database files must be
deleted first, as the script recreates the entire table.

This is a replacement of network.py in Lakbay v1.0. Some parts of the code
have been adapted from the aformentioned file.

:Author:     Maded Batara III
:Version:    v1.0 (2016-03-25)
"""

# Folder containing GTFS files
GTFS_FOLDER = "data/gtfs-sakay"

# Create engine and session
engine = create_engine('sqlite:///app.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# TABLE stops
# (1) stops.txt
stops_table = []
with open("../{0}/stops.txt".format(GTFS_FOLDER)) as stops_file:
    stops = csv.reader(stops_file)
    for stop in stops:
        # Disregard first row
        if stop[2] != "stop_name":
            stops_table.append(Stop(
                stop[2],
                float(stop[4]),
                float(stop[5]),
                stop[0]
            ))
session.add_all(stops_table)

# TABLE routes
# (1) trips.txt
routes_table = []
with open("../{0}/trips.txt".format(GTFS_FOLDER)) as trips_file:
    trips = csv.reader(trips_file)
    for trip in trips:
        # Disregard first row
        if trip[0] != "route_id":
            routes_table.append(Route(
                None,
                None,
                trip[-1],
                trip[0],
                trip[1]
            ))
session.add_all(routes_table)
# (2) routes.txt
with open("../{0}/routes.txt".format(GTFS_FOLDER)) as routes_file:
    routes = csv.reader(routes_file)
    for route in routes:
        for row in session.query(Route).filter(Route.route_id == route[-1]):
            row.name = route[2]
            row.description = route[3]
# (3) Walking
session.add(Route(
    "Walking",
    "A general-purpose route for walking.",
    "000001",
    "ROUTE_WALKING",
    "000001"
))

# TABLE frequencies
# (1) frequencies.txt
with open("../{0}/frequencies.txt".format(GTFS_FOLDER)) as frequencies_file:
    frequencies = csv.reader(frequencies_file)
    for frequency in frequencies:
        for row in session.query(Route).filter(Route.trip_id == frequency[0]):
            row.frequency = RouteFrequency(
                datetime.datetime.strptime(frequency[1], '%H:%M:%S').time(),
                datetime.datetime.strptime(frequency[2], '%H:%M:%S').time(),
                int(frequency[3]),
                None, None, None, None, None, None, None
            )
# (2) calendar.txt
with open("../{0}/calendar.txt".format(GTFS_FOLDER)) as calendar_file:
    calendars = csv.reader(calendar_file)
    for calendar in calendars:
        for row in session.query(Route).filter(
                   Route.service_id == calendar[0]):
            row.frequency.mon = bool(int(calendar[1]))
            row.frequency.tue = bool(int(calendar[2]))
            row.frequency.wed = bool(int(calendar[3]))
            row.frequency.thu = bool(int(calendar[4]))
            row.frequency.fri = bool(int(calendar[5]))
            row.frequency.sat = bool(int(calendar[6]))
            row.frequency.sun = bool(int(calendar[7]))

# TABLE graph
# (1) stop_times.txt
graph_table = []
previous = None
with open("../{0}/stop_times.txt".format(GTFS_FOLDER)) as stop_times_file:
    stop_times = csv.reader(stop_times_file)
    for current in stop_times:
        if current[0] != "trip_id" and previous[0] == current[0]:
            time_delta = datetime.datetime.strptime(
                current[3], '%H:%M:%S') - datetime.datetime.strptime(
                previous[4], '%H:%M:%S')
            graph_table.append(Edge(
                session.query(Stop).filter(
                    Stop.stop_id == previous[2]).first(),
                session.query(Stop).filter(
                    Stop.stop_id == current[2]).first(),
                session.query(Route).filter(
                    Route.trip_id == current[0]).first(),
                int(previous[1]),
                int(time_delta.total_seconds())
            ))
        previous = current
session.add_all(graph_table)

# Close connection
session.commit()
session.close()
