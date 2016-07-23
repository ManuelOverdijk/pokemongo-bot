from functools import partial
from random import uniform
from geopy.distance import vincenty

from POGOProtos.Inventory.ItemId_pb2 import _ITEMID
import POGOProtos.Networking.Requests_pb2 as Requests
from processors import make_request, process_request
from utils.pgoexceptions import BotModuleException
from utils.settings import STEP_SIZE_POLAR, STEP_SIZE_METERS


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
        print 'Teleporting...'
        self._player.lat = lat
        self._player.lon = lon
        return True

    @task
    def step_towards(self, lat, lon):
        print 'Walking...'
        delta_lat = lat - self._player.lat
        delta_lon = lon - self._player.lon
        ratio = delta_lat / delta_lon

        self._player.lat += ratio * STEP_SIZE_POLAR
        self._player.lon += (1 - ratio) * STEP_SIZE_POLAR
        return True

    @task
    def encounter_pokemon(self, encounter_id, spawn_point_id):
        params = {'encounter_id': encounter_id, 'spawn_point_id': spawn_point_id,
                  'player_latitude': self._player.lat,
                  'player_longitude': self._player.lon}
        request = make_request(Requests.ENCOUNTER, params=params)
        answer = process_request(self._rpc_client, request)
        if answer and answer.status == 1:
            print 'Encounter successful!'
        else:
            print 'Encounter failed!'

    @task
    def catch_pokemon(self, encounter_id, spawn_point_id):
        params = {'encounter_id': encounter_id,
                  'spawn_point_guid': spawn_point_id,
                  'pokeball': 1,
                  'hit_pokemon': True,
                  'spin_modifier': 1,
                  'normalized_reticle_size': uniform(0.8, 1.95),
                  'normalized_hit_position': 1}
        request = make_request(Requests.CATCH_POKEMON, params=params)
        answer = process_request(self._rpc_client, request)
        if answer and answer.status == 1:
            print 'Catch successful'
        else:
            print 'Catch failed'
        pass

    def get_fort_details(self, fort_id, latitude, longitude):
        params = {'fort_id': fort_id,
                  'latitude': latitude,
                  'longitude': longitude}
        request = make_request(Requests.FORT_DETAILS, params=params)
        answer = process_request(self._rpc_client, request)
        return answer

    @task
    def search_fort(self, fort_id, fort_lat, fort_lon):
        params = {'fort_id': fort_id,
                  'fort_latitude': fort_lat,
                  'fort_longitude': fort_lon,
                  'player_latitude': self._player.lat,
                  'player_longitude': self._player.lon}
        request = make_request(Requests.FORT_SEARCH, params=params)
        answer = process_request(self._rpc_client, request)
        if answer.result == 1:
            item_ids = [_ITEMID.values_by_number[item.item_id].name for
                          item in answer.items_awarded]
            print 'Received items: ' +\
                  ', '.join([''.join([i.title() for i in item_id.split('_')[1:]]) +\
                  ' x{0}'.format(item_ids.count(item_id)) for item_id in set(item_ids)])
        else:
            print 'Search failed'

    def _distance_between(self, point1, point2):
        return vincenty(point1, point2).meters

    def _player_distance_to(self, point):
        return self._distance_between((self._player.lat, self._player.lon),
                                     point)
