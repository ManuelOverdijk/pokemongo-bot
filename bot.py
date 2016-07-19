from geopy.geocoders import GoogleV3

from utils.rpc_client import RpcClient
from utils.structures import Data, Player


class Bot:
    data = Data()
    player = Player()
    rpc_client = None

    def __init__(self, token, location_name):
        geolocator = GoogleV3()
        position = geolocator.geocode(location_name)
        self.player.lat = position.latitude
        self.player.lon = position.longitude
        self.rpc_client = RpcClient(token, self.player)
