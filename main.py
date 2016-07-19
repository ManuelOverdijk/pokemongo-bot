from getpass import getpass

from bot import Bot
from utils.auth import PtcAuth

if __name__ == '__main__':
    login_type = {
        'google': None,
        'ptc': PtcAuth
    }[raw_input('Which login provider do you want to '
                'use (google/ptc)? [ptc]: ') or 'ptc']

    username = raw_input('Username: ')
    password = getpass()
    location = raw_input('Where do you want to spawn? '
                         '[New York, NY, USA]: ') or 'New York, NY, USA'

    try:
        token = login_type().get_auth_token(username, password)
        bot = Bot(token, location)
    except ValueError as error:
        print(error)
        exit(1)
