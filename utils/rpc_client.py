

class RpcClient:
    token = None
    player = None

    def __init__(self, token, player):
        self.token = token
        self.player = player