from functools import partial
from geopy.distance import vincenty
from math import sin, cos, atan2, sqrt

from POGOProtos.Networking.Requests.Messages.EncounterMessage_pb2 import EncounterMessage
from POGOProtos.Networking.Requests.Messages.CatchPokemonMessage_pb2 import CatchPokemonMessage
from POGOProtos.Networking.Responses.EncounterResponse_pb2 import EncounterResponse

from utils.settings import STEP_SIZE_POLAR, STEP_SIZE_METERS


class BaseModule(object):

    def __init__(self, priority=1):
        self.priority = priority

    def __injectmodule__(self, player, data, rpc_client):
        self.__player = player
        self.__data = data
        self.__rpc_client = rpc_client

    def teleport_to(self, lat, lon):
        def wrapper(lat, lon):
            self.__player.lat = lat
            self.__player.lon = lon
            return True
        return [partial(wrapper, lat, lon)]

    def walk_to(self, lat, lon):
        distance = self._player_distance_to(lat, lon)
        return [self.step_towards(lat, lon) for step in
                range(int(distance / STEP_SIZE_METERS))]

    def step_towards(self, lat, lon):
        def wrapper(lat, lon):
            delta_lat = lat - self.__player.lat
            delta_lon = lon - self.__player.lon
            ratio = delta_lat / delta_lon

            self.__player.lat += ratio * STEP_SIZE_POLAR
            self.__player.lon += (1 - ratio) * STEP_SIZE_POLAR
            return True

        return [partial(wrapper, lat, lon)]

    def encounter_pokemon(self, encounter_id, spawnpoint_id):
        def wrapper(encounter_id, spawnpoint_id):
            encounter = EncounterMessage()
            encounter.encounter_id = encounter_id
            encounter.spawnpoint_id = spawnpoint_id
            encounter.player_latitude = self.__player.lat
            encounter.player_longitude = self.__player.lon

            encounter_response = self.__rpc_client.get_response(encounter,
                                                                EncounterResponse)
            ## TODO: check encounter_response and return False if something
            #  is wrong, so the currently executing Task is stopped.
            return True

        return [partial(wrapper, encounter_id, spawnpoint_id)]

    def catch_pokemon(self, encounter_id):
        self.__rpc_client
        pass

    def _distance_between(self, point1, point2):
        return vincenty(point1, point2).meters

    def _player_distance_to(self, point):
        return self.distance_between((self.__player.lat, self.__player.lon), point)
