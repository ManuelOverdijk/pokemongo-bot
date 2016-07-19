from functools import partial
from math import sin, cos, atan2, sqrt

from utils.settings import STEP_SIZE_POLAR, STEP_SIZE_METERS


class BaseModule:
    data = None
    player = None
    rpc_client = None
    priority = 1

    def __init__(self, data, player, rpc_client):
        self.data = data
        self.player = player
        self.rpc_client =rpc_client
        pass

    def teleport_to(self, lat, lon):
        def wrapper(lat, lon):
            self.player.lat = lat
            self.player.lon = lon
        return [partial(wrapper, lat, lon)]

    def walk_to(self, lat, lon):
        distance = self._player_distance_to(lat, lon)
        return [self.step_towards(lat, lon) for step in
                range(int(distance / STEP_SIZE_METERS))]

    def step_towards(self, lat, lon):
        def wrapper(lat, lon):
            delta_lat = lat - self.player.lat
            delta_lon = lon - self.player.lon
            ratio = delta_lat / delta_lon

            self.player.lat += ratio * STEP_SIZE_POLAR
            self.player.lon += (1 - ratio) * STEP_SIZE_POLAR

        return [partial(wrapper, lat, lon)]

    def catch_pokemon(self, encounter_id):
        self.rpc_client
        pass

    def _distance_between(self, lat1, lon1, lat2, lon2):
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = (sin(dlat / 2)) ^ 2 + cos(lat1) * cos(lat2) * (sin(dlon / 2)) ^ 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        d = 6371 * c  # 6,371 is the earth's circumference in km
        return d / 1000  # divide to turn into meters

    def _player_distance_to(self, lat, lon):
        return self.distance_between(lat, lon, self.player.lat,
                                     self.player.lon)
