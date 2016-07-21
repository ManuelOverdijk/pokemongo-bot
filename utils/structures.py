class Data(object):
    def __init__(self):
        self.nearby_pokemon = []


class Player(object):
    def __init__(self, latitude, longitude, altitude):
        self.lat = latitude
        self.lon = longitude
        self.alt = altitude
