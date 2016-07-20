from functools import partial
from geopy.distance import vincenty
from math import sin, cos, atan2, sqrt

from utils.settings import STEP_SIZE_POLAR, STEP_SIZE_METERS


class BaseModule:
    
    def __init__(self, data, player, rpc_client):
        self.data = data
        self.player = player
        self.rpc_client = rpc_client
        self.priority = 1
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

    def _distance_between(self, point1, point2):
        return vincenty(point1, point2).meters

    def _player_distance_to(self, point):
        return self.distance_between((self.player.lat, self.player.lon), point)
