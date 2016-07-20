from getpass import getpass

from bot import Bot, RandomizedTaskScheduler
from utils.auth import PtcAuth
from utils.rpc_client import RpcClient
from utils.structures import Player
from utils.pgoexceptions import AuthenticationException, RpcException
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
        position = geolocator.geocode(location)
        player = Player(position.latitude, position.longitude)
        rpc = RpcClient(player)

        login_session = login_type()
        if login_session.login(username, password):
            if rpc.authenticate(login_session):
                print "[RPC] Authenticated"
                scheduler = RandomizedTaskScheduler()
                bot = Bot(rpc, scheduler)
            else:
                print "[RPC] Failed to authenticate"
        else:
            print "[LOGIN] Login failed, check your username and password"
    except AuthenticationException as error:
        print(error)
    except RpcException as error:
        print(error)
    except ValueError as error:
        print(error)
        exit(1)
