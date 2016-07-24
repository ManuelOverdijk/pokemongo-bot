class Data(object):
    def __init__(self):
        self.catchable_pokemon = []
        self.nearby_pokemon = []
        self.wild_pokemon = []
        self.decimated_spawn_points = []
        self.spawn_points = []
        self.fort_summaries = []
        self.forts = []


class Player(object):
    def __init__(self, latitude, longitude, altitude):
        self.lat = latitude
        self.lon = longitude
        self.alt = altitude
        self.pokemon = []
        self.inventory = []
