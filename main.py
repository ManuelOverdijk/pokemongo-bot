#!/usr/bin/python

import json
from getpass import getpass

from geopy.geocoders import GoogleV3

from bot import Bot
from schedulers import RandomizedTaskScheduler
from utils.auth import PtcAuth
from utils.rpc_client import RpcClient
from utils.structures import Player
from modules.idle import IdleModule
from modules.inventory_maintenance import InventoryMaintenanceModule
from modules.catch_pokemon import CatchPokemonModule
from modules.visit_pokestop import VisitPokestopModule

def get_settings():
    try:
        with open('settings.json') as file:
            settings = json.load(file)
    except IOError as error:
        provider = raw_input('Which login provider do you want to '
                             'use (google/ptc)? [ptc]: ') or 'ptc'

        username = raw_input('Username: ')
        password = getpass()
        location = raw_input('Where do you want to spawn? '
                             '[New York, NY, USA]: ') or 'New York, NY, USA'
        geolocator = GoogleV3()
        position = geolocator.geocode(location)
        settings = dict(username=username, password=password,
                        location=location, provider=provider,
                        latitude=position.latitude,
                        longitude=position.longitude,
                        altitude=position.altitude)

        with open('settings.json', 'w') as outfile:
            json.dump(settings, outfile)

    return settings


if __name__ == '__main__':
    settings = get_settings()
    login_type = {
        'google': None,
        'ptc': PtcAuth
    }[settings['provider']]

    player = Player(settings['latitude'], settings['longitude'],
                    settings['altitude'])
    rpc = RpcClient(player)

    login_session = login_type()
    if login_session.login(settings['username'], settings['password']):
        if rpc.authenticate(login_session):
            print '[RPC] Authenticated'
            scheduler = RandomizedTaskScheduler()
            bot = Bot(rpc, scheduler)
            bot.add_modules([
                IdleModule(priority=5),
                VisitPokestopModule(priority=300),
                CatchPokemonModule(priority=500),
                InventoryMaintenanceModule(priority=1000)
            ])
            bot.run_loop()
        else:
            print '[RPC] Failed to authenticate'
    else:
        print '[LOGIN] Login failed, check your username and password'
