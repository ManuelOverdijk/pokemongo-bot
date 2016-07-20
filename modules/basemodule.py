from functools import partial
from geopy.distance import vincenty

from POGOProtos.Networking.Requests.Messages_pb2 import (
    EncounterMessage,
    CatchPokemonMessage
)
from POGOProtos.Networking.Responses_pb2 import (
    EncounterResponse
)

from utils.settings import STEP_SIZE_POLAR, STEP_SIZE_METERS

def task(function):
    def wrapper(*args, **kwargs):
        return [partial(function, *args, **kwargs)]
    return wrapper

class BaseModule(object):

    def __init__(self, priority=1):
        self.priority = priority

    def __injectmodule__(self, player, data, rpc_client):
        self._player = player
        self._data = data
        self.__rpc_client = rpc_client

    @task
    def teleport_to(self, lat, lon):
        self._player.lat = lat
        self._player.lon = lon
        return True

    def walk_to(self, lat, lon):
        distance = self._player_distance_to(lat, lon)
        return [self.step_towards(lat, lon) for step in
                range(int(distance / STEP_SIZE_METERS))]

    @task
    def step_towards(self, lat, lon):
        delta_lat = lat - self._player.lat
        delta_lon = lon - self._player.lon
        ratio = delta_lat / delta_lon

        self._player.lat += ratio * STEP_SIZE_POLAR
        self._player.lon += (1 - ratio) * STEP_SIZE_POLAR
        return True

    @task
    def encounter_pokemon(self, encounter_id, spawnpoint_id):
        encounter = EncounterMessage()
        encounter.encounter_id = encounter_id
        encounter.spawnpoint_id = spawnpoint_id
        encounter.player_latitude = self._player.lat
        encounter.player_longitude = self._player.lon

        encounter_response = self.__rpc_client.get_response(encounter,
                                                            EncounterResponse)
        ## TODO: check encounter_response and return False if something
        #  is wrong, so the currently executing Task is stopped.
        return True

    def catch_pokemon(self, encounter_id):
        self.__rpc_client
        pass

    def _distance_between(self, point1, point2):
        return vincenty(point1, point2).meters

    def _player_distance_to(self, point):
        return self.distance_between((self._player.lat, self._player.lon), point)
