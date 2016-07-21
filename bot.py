from utils.rpc_client import RpcClient
from utils.structures import Data, Player
from utils.task import Task
from processors import make_request, process_request, process_requests
import POGOProtos.Networking.Requests_pb2 as Requests


class Bot(object):

    def __init__(self, rpc, scheduler):
        self.rpc_client = rpc
        self.data = Data()
        self.__scheduler = scheduler
        self.__modules = []

    @property
    def player(self):
        return self.rpc_client.player

    def run_loop(self):
        self.__initial_message()
        while True:
            successful = self.__update_heartbeat()
            tasks = []
            for mod in self.__modules:
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
        reqs = [
            make_request(Requests.GET_PLAYER),
            make_request(Requests.GET_HATCHED_EGGS),
            make_request(Requests.GET_INVENTORY),
            make_request(Requests.CHECK_AWARDED_BADGES),
            make_request(Requests.DOWNLOAD_SETTINGS, params={
                         'hash': '05daf51635c82611d1aac95c0b051d3ec088a930'})
        ]
        process_requests(self.rpc_client, reqs)

    def __update_heartbeat(self):
        ## TODO: implement correct heartbeat
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
