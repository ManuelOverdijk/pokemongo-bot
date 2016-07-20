
from utils.rpc_client import RpcClient
from utils.structures import Data, Player


class Bot:
    def __init__(self, rpc):
        self.player = rpc.player
        self.data = Data()
        self.rpc_client = rpc

    # def run_loop(self):
    #     while True:
