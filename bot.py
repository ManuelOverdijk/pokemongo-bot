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
                    'Bot.add_modules: module %s already added' % repr(mod)
                )
            injected = self.__inject_module(mod)
            self.__modules.append((idm, injected))
            idm += 1

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

    # def run_loop(self):
    #     while True:


## TODO:
# [1] Task interface preliminary, needs to be made concrete
# [2] Move scheduler into separate module and move execution_step into
#     a base class
class RandomizedTaskScheduler(object):
    def __init__(self):
        self._current_task = None

    def update_tasks(self, tasks):
        from random import shuffle
        shuffled = tasks[:]
        shuffle(shuffled)

        max_priority, _, selected_task = shuffled[0]
        for priority, _, task in shuffled:
            if priority > max_priority:
                max_priority = priority
                selected_task = task

        if (
            max_priority > self.__current_task.priority
            or self._current_task.isdone
        ):
            self._current_task = selected_task

    def execution_step(self):
        ## TODO: check task interface (partials.pop())
        #
        next_task = self._current_task.partials.pop()
        next_task()
