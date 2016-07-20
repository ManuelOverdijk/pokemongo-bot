
from utils.rpc_client import RpcClient
from utils.structures import Data, Player


class Bot(object):
    def __init__(self, rpc, scheduler):
        self.rpc_client = rpc
        self.data = Data()
        self.__scheduler = scheduler
        self.__modules = []

    @property
    def player(self):
        return self.rpc_client.player

    def add_module(self, module):
        self.add_modules([module])

    def add_modules(self, modules):
        idm = len(self.__modules)
        for mod in modules:
            if self.__module_exists(mod):
                raise ValueError(
                    'Bot.add_modules: module already added'
                )
            self.__modules.append((idm, mod))
            idm += 1

    def __module_exists(self, module):
        module_classes = [mod.__class__ for _, mod in self.__modules]
        return module.__class__ in module_classes

    # def run_loop(self):
    #     while True:

class RandomizedTaskScheduler(object):

    def __init__(self):
        pass

    def select_task(self, tasks):
        from random import shuffle
        shuffled = tasks[:]
        shuffle(shuffled)

        max_priority, _, selected_task = shuffled[0]
        for priority, _, task in shuffled:
            if priority > max_priority:
                max_priority = priority
                selected_task = task

        return selected_task
