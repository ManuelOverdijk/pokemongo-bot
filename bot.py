
from utils.rpc_client import RpcClient
from utils.structures import Data, Player


class Bot:
    def __init__(self, rpc):
        self.rpc_client = rpc
        self.data = Data()

    @property
    def player(self):
        return self.rpc_client.player

    # def run_loop(self):
    #     while True:
