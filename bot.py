from utils.rpc_client import RpcClient
from utils.structures import Data, Player
from utils.task import Task
from processors import make_request, process_request
import POGOProtos.Networking.Requests.Messages_pb2 as Messages


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

    def __update_heartbeat(self):
        ## TODO: implement correct heartbeat with processors
        #
        #heartbeat = make_request(
        #    Messages.GetMapObjectsMessage, self.player, self._data)
        heartbeat = None
        return process_request(self.rpc_client, heartbeat)

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
