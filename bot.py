
from utils.rpc_client import RpcClient
from utils.structures import Data, Player


class Bot(object):
    def __init__(self, rpc):
        self.rpc_client = rpc
        self.data = Data()

    @property
    def player(self):
        return self.rpc_client.player

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
