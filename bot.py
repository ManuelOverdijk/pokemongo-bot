from time import time

import POGOProtos.Networking.Requests_pb2 as Requests
from processors import make_request, process_request, process_requests
from utils.structures import Data
from utils.task import Task
from utils.map import get_neighbours


class Bot(object):
    def __init__(self, rpc, scheduler):
        self.rpc_client = rpc
        self.data = Data()
        self.__scheduler = scheduler
        self.__modules = []
        self.__last_update = 0

    @property
    def player(self):
        return self.rpc_client.player

    def run_loop(self):
        self.__initial_message()
        while True:
            successful = self.__update_map_objects()
            tasks = []
            for _, mod in self.__modules:
                task_queue = mod.execute()
                if task_queue:
                    tasks.append(Task(task_queue, mod.priority))
            if tasks:
                self.__scheduler.update_tasks(tasks)
            self.__scheduler.execute_step()

    def add_modules(self, modules):
        for mod in modules:
            if self.__module_exists(mod):
                raise ValueError(
                    'Bot.add_modules: module %s already added' % repr(mod)
                )
            injected = self.__inject_module(mod)
            self.__modules.append((injected.__class__, injected))

    def __initial_message(self):
        process_request(self.rpc_client, make_request(Requests.GET_PLAYER))
        reqs = [
            make_request(Requests.GET_PLAYER),
            make_request(Requests.GET_HATCHED_EGGS),
            make_request(Requests.GET_INVENTORY),
            make_request(Requests.CHECK_AWARDED_BADGES),
            make_request(Requests.DOWNLOAD_SETTINGS, params={
                'hash': '05daf51635c82611d1aac95c0b051d3ec088a930'})
        ]
        result = process_requests(self.rpc_client, reqs)
        pass

    def __update_map_objects(self):
        cell_ids = get_neighbours(self.player.lat, self.player.lon)
        request = make_request(Requests.GET_MAP_OBJECTS, params={
            'cell_id': cell_ids,
            'since_timestamp_ms': [self.__last_update] * len(cell_ids),
            'latitude': self.player.lat,
            'longitude': self.player.lon
        })
        response = process_request(self.rpc_client, request)

        ## TODO: probably update our state in another method
        self.__last_update = int(time())
        attribs = {
            'catchable_pokemon': 'catchable_pokemons',
            'wild_pokemon': 'wild_pokemons',
            'nearby_pokemon': 'nearby_pokemons',
            'decimated_spawn_points': 'decimated_spawn_points',
            'spawn_points': 'spawn_points',
            'forts': 'forts',
        }

        for attrib in attribs:
            setattr(self.data, attrib, [])

        for map_cell in response.map_cells:
            for our_attrib, pb_attrib in attribs.items():
                value = getattr(self.data, our_attrib)
                value += getattr(map_cell, pb_attrib)

        pass

    def __inject_module(self, module):
        try:
            module.__injectmodule__(self.player, self.data, self.rpc_client)
            return module
        except:
            raise ValueError(
                'Bot.add_modules: %s not a module' % repr(module)
            )

    def __module_exists(self, module):
        module_classes = [mod.__class__ for _, mod in self.__modules]
        return module.__class__ in module_classes
