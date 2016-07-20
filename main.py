from getpass import getpass

from bot import Bot
from utils.auth import PtcAuth
from utils.rpc_client import RpcClient
from utils.structures import Player
from geopy.geocoders import GoogleV3

if __name__ == '__main__':
    provider = raw_input('Which login provider do you want to '
                'use (google/ptc)? [ptc]: ') or 'ptc'

    login_type = {
        'google': None,
        'ptc': PtcAuth
    }[provider]

    username = raw_input('Username: ')
    password = getpass()
    location = raw_input('Where do you want to spawn? '
                         '[New York, NY, USA]: ') or 'New York, NY, USA'

    try:
        geolocator = GoogleV3()
        token = login_type().get_auth_token(username, password)

        position = geolocator.geocode(location)
        player = Player(position.latitude, position.longitude)
        rpc = RpcClient(player)
        if rpc.authenticate(token, provider):
            print "[RPC] Authenticated"
            bot = Bot(rpc)
        else:
            print "[RPC] Failed to authenticate"
    except ValueError as error:
        print(error)
        exit(1)
