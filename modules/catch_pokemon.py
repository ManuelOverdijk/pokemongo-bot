from POGOProtos.Enums_pb2 import _POKEMONID
from basemodule import BaseModule, task
from utils.settings import PARANOID_MODE


class CatchPokemonModule(BaseModule):
    def execute(self):
        catchable = self._data.catchable_pokemon
        wild = self._data.wild_pokemon
        pokemon = self._find_best_pokemon(catchable, wild)

        if pokemon:
            move_method = self.walk_to if PARANOID_MODE else self.teleport_to
            return (self.print_target_name(pokemon) +
                    move_method(pokemon.latitude, pokemon.longitude) +
                    self.encounter_pokemon(pokemon.encounter_id,
                                           pokemon.spawn_point_id) +
                    self.catch_pokemon(pokemon.encounter_id,
                                       pokemon.spawn_point_id))

    @task
    def print_target_name(self, pokemon):
        name = _POKEMONID.values_by_number[pokemon.pokemon_id].name.title()
        print('Going to catch a %s.' % name)

    def _find_best_pokemon(self, catchable, wild):
        ## Naive behaviour: since we don't have access to the Pokemon's
        #  CP stats, just return the closest one
        unsorted_pokemon = catchable if len(catchable) > 0 else wild
        if len(unsorted_pokemon):
            sorted_pokemon = sorted(catchable, key=lambda pokemon:
                self._player_distance_to((pokemon.latitude, pokemon.longitude)))
            return sorted_pokemon[0]
        else:
            return None
