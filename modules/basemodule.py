from functools import partial
from geopy.distance import vincenty
from processors import make_request, process_request

from POGOProtos.Networking.Requests.Messages_pb2 import (
    EncounterMessage,
    CatchPokemonMessage
)
from POGOProtos.Networking.Responses_pb2 import (
    EncounterResponse
)

from utils.settings import STEP_SIZE_POLAR, STEP_SIZE_METERS
from pgoexceptions import BotModuleException


def task(function):
    def wrapper(*args, **kwargs):
        return [partial(function, *args, **kwargs)]

    return wrapper


class BaseModule(object):
    def __init__(self, priority=1):
        self.priority = priority
        if not hasattr(self, 'execute'):
            raise BotModuleException(
                ('Module %s does not appear to have an execute method ' +
                'defined.') % self.__class__.__name__
            )

    def __injectmodule__(self, player, data, rpc_client):
        self._player = player
        self._data = data
        self._rpc_client = rpc_client

    def walk_to(self, lat, lon):
        distance = self._player_distance_to(lat, lon)
        return [self.step_towards(lat, lon) for step in
                range(int(distance / STEP_SIZE_METERS))]

    @task
    def teleport_to(self, lat, lon):
        self._player.lat = lat
        self._player.lon = lon
        return True

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
        params = {'encounter_id': encounter_id, 'spawnpoint_id': spawnpoint_id,
                  'player_latitude': self._player.lat,
                  'player_longitude': self._player.lon}
        request = make_request(EncounterMessage, params=params)
        answer = process_request(self._rpc_client, request)
        if answer:
            print 'Encounter successful!'
        else:
            print 'Encounter failed!'

    def catch_pokemon(self, encounter_id):
        self._rpc_client
        pass

    def _distance_between(self, point1, point2):
        return vincenty(point1, point2).meters

    def _player_distance_to(self, point):
        return self.distance_between((self._player.lat, self._player.lon),
                                     point)
