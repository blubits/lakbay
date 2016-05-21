from db.models import Route, Stop

"""
A human-readable format for a series of routes that
make up a trip between two destinations.

:Author:     Maded Batara III
:Version:    v1.1 (2015-12-29)
"""

# Walking route ID
WALKING_ROUTE_ID = "000001"

class Trip:

    def __init__(self, network, route_list):
        """
        Creates a trip from a set of routes.

        Args:
            network (Network): A transport network, where the routes listed
                operate on.
            route_list (list): A list of dictionaries that describe the trip
                supposed to be taken. See route_parser.py.
        """
        self._network = network
        self._route_list = route_list
        self._travel_time = sum(route["travel_time"] for route in route_list)

    def __str__(self):
        """
        Returns str(self).
        """
        route_strings = ["Trip takes {0}min {1}s total".format(
            self.travel_time // 60,
            self.travel_time % 60
        )]
        counter = 1
        for route in self._route_list:
            route_id = route["route_id"]
            fr, to = route["from"], route["to"]
            travel_time = route["travel_time"]
            route_string = "{0}. {1} (takes {4}min {5}s)" \
                           "\n\tFrom: {2} ({6})\n\tTo: {3} ({7})".format(
                               counter,
                               self._network.routes.filter(
                                   Route.id == route_id).first().name,
                               self._network.stops.filter(
                                   Stop.id == fr).first().name,
                               self._network.stops.filter(
                                   Stop.id == to).first().name,
                               travel_time // 60,
                               travel_time % 60, fr, to)
            route_strings.append(route_string)
            counter += 1
        return "\n".join(route_strings)

    def __repr__(self):
        """
        Returns repr(self).
        """
        return "<class Trip, {0}->{1} ({2}min {3}s)>".format(
            self._route_list[0]["from"],
            self._route_list[-1]["to"],
            self._travel_time // 60,
            self._travel_time % 60
        )

    @property
    def route_list(self):
        """
        List of routes to be taken.
        """
        return self._route_list

    @property
    def network(self):
        """
        Transport network where routes operate.
        """
        return self._network

    @property
    def travel_time(self):
        """
        Total travel time of trip.
        """
        return self._travel_time

    def to_json(self):
        """
        Returns a JSON representation of the trip.
        """
        json = {}
        json["total_travel_time"] = self._travel_time
        json["routes"] = []
        for route in self._route_list:
            # Get replaced route if route is "walking"
            if route["route_id"] == WALKING_ROUTE_ID:
                route_obj = self._network.get_route_by_id(
                    route["modified_route_id"]
                )
            else:
                route_obj = self._network.get_route_by_id(
                    route["route_id"]
                )
            fr, to = route["from"], route["to"]
            route_json = self._network.get_route_by_id(
                route["route_id"]
            ).to_json()
            json["routes"].append({
                "route": {
                    "name": route_json["name"],
                    "type": route_json["type"],
                    "color": route_json["color"]
                },
                "node_path": [{
                    "name": self._network.stops[node].to_json()["name"],
                    "lat": self._network.stops[node].to_json()["lat"],
                    "lng": self._network.stops[node].to_json()["lng"]
                } for node in route_obj.splice(fr, to)]
            })
        return json
