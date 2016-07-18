from math import sin, cos, atan2, sqrt

from settings import STEP_SIZE


class BaseModule:
    data = None
    player = None

    def __init__(self, data, player):
        """

        :param data:
        :param player:
        """
        self.data = data
        self.player = player
        pass

    def step_towards(self, lat, lon):
        """

        :param lat:
        :param lon:
        :return:
        """
        delta_lat = lat - self.player.lat
        delta_lon = lon - self.player.lon
        ratio = delta_lat / delta_lon

        self.player.lat += ratio * STEP_SIZE
        self.player.lon += (1 - ratio) * STEP_SIZE

    def teleport_to(self, lat, lon):
        """

        :param lat:
        :param lon:
        :return:
        """
        self.player.lat = lat
        self.player.lon = lon

    def distance_between(self, lat1, lon1, lat2, lon2):
        """

        :param lat1:
        :param lon1:
        :param lat2:
        :param lon2:
        :return:
        """
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = (sin(dlat / 2)) ^ 2 + cos(lat1) * cos(lat2) * (sin(dlon / 2)) ^ 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        d = 6371 * c  # 6,371 is the earth's circumference in km
        return d

    def player_distance_to(self, lat, lon):
        """

        :param lat:
        :param lon:
        :return:
        """
        return self.distance_between(lat, lon, self.player.lat,
                                     self.player.lon)
