import csv
import datetime
from models import Stop, Route, RouteFrequency, Base
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker

"""
Database creator from the GTFS class.

As this is a database creator, should only be executed when there is an
update in the underlying data source. The existing database files must be
deleted first, as the script recreates the entire table.

This is a replacement of network.py in Lakbay v1.0. Some parts of the code
have been adapted from the aformentioned file.

:Author:     Maded Batara III
:Version:    v1.0dev (2016-03-25)
"""

# Folder containing GTFS files.
GTFS_FOLDER = "data/gtfs-sakay"

# Create engine and session
engine = create_engine('sqlite:///app.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# TABLE stops
# (1) stops.txt
stop_table = []
with open("../{0}/stops.txt".format(GTFS_FOLDER)) as stops_file:
    stops = csv.reader(stops_file)
    for stop in stops:
        # Disregard first row
        if stop[2] != "stop_name":
            stop_table.append(Stop(
                stop[2],
                float(stop[4]),
                float(stop[5]),
                stop[0]
            ))
session.add_all(stop_table)

# TABLE routes
# (1) trips.txt
route_table = []
with open("../{0}/trips.txt".format(GTFS_FOLDER)) as trips_file:
    trips = csv.reader(trips_file)
    for trip in trips:
        # Disregard first row
        if trip[0] != "route_id":
            route_table.append(Route(
                None,
                None,
                trip[-1],
                trip[0],
                trip[1]
            ))
session.add_all(route_table)
# (2) routes.txt
with open("../{0}/routes.txt".format(GTFS_FOLDER)) as routes_file:
    routes = csv.reader(routes_file)
    for route in routes:
        for row in session.query(Route).filter(Route.route_id == route[-1]):
            row.name = route[2]
            row.description = route[3]

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
        for row in session.query(Route).filter(Route.service_id == calendar[0]):
            row.frequency.mon = bool(int(calendar[1]))
            row.frequency.tue = bool(int(calendar[2]))
            row.frequency.wed = bool(int(calendar[3]))
            row.frequency.thu = bool(int(calendar[4]))
            row.frequency.fri = bool(int(calendar[5]))
            row.frequency.sat = bool(int(calendar[6]))
            row.frequency.sun = bool(int(calendar[7]))

session.commit()
session.close()
