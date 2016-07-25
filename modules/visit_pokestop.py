from basemodule import BaseModule, task
from utils.settings import PARANOID_MODE, MAX_ITEMS
import POGOProtos.Map.Fort_pb2 as Forts

class VisitPokestopModule(BaseModule):

    def __init__(self, priority):
        super(VisitPokestopModule, self).__init__(priority=priority)
        ## TODO: save timestamp of when the stop is valid again after searching
        self._recent_stops = []

    def execute(self):
        total_items = sum([item.count for item in self._player.inventory])
        if total_items >= MAX_ITEMS:
            return

        forts = self._data.forts
        pokestops = [fort for fort in forts if fort.type == Forts.CHECKPOINT and
                     not self._searched_recently(fort)]
        sorted_pokestops = sorted(pokestops, key=lambda pokestop:
                            self._player_distance_to((pokestop.latitude,
                                  pokestop.longitude)))

        if len(sorted_pokestops) > 0:
            pokestop = sorted_pokestops[0]  # Nearest PokeStop
            move_method = self.walk_to if PARANOID_MODE else self.teleport_to
            return (self.print_target_pokestop(pokestop) +
                    move_method(pokestop.latitude, pokestop.longitude) +
                    self.search_fort(pokestop.id, pokestop.latitude,
                                     pokestop.longitude)+
                    self.save_pokestop_search(pokestop))

    @task
    def print_target_pokestop(self, pokestop):
        details = self.get_fort_details(pokestop.id, pokestop.latitude,
                                        pokestop.longitude)
        print('Going to visit PokeStop "%s"' % details.name)

    @task
    def save_pokestop_search(self, pokestop):
        self._recent_stops.append(pokestop.id)

    def _searched_recently(self, pokestop):
        return pokestop.id in self._recent_stops
