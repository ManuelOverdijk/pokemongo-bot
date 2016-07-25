from basemodule import BaseModule, task
import POGOProtos.Networking.Requests_pb2 as Requests
from processors import make_request, process_requests
from utils.settings import MAX_POKEMON


class InventoryMaintenanceModule(BaseModule):

    def execute(self):
        caught_pokemon = self._player.pokemon
        if len(caught_pokemon) >= (MAX_POKEMON - 10) and \
            len(caught_pokemon) != len(self._get_best_pokemon()):
            return self.remove_low_cp_pokemon()

    @task
    def remove_low_cp_pokemon(self):
        print 'Purging lowest CP pokemon'
        best_pokemon = self._get_best_pokemon()
        purged_pokemon = []
        for pokemon in self._player.pokemon:
            pokemon_id = pokemon.pokemon_id
            if best_pokemon[pokemon_id].id != pokemon.id:
                purged_pokemon.append(pokemon)
        self._transfer_pokemon(purged_pokemon)

    def _get_best_pokemon(self):
        best_pokemon = {}
        for pokemon in self._player.pokemon:
            pokemon_id = pokemon.pokemon_id
            if pokemon_id not in best_pokemon:
                best_pokemon[pokemon_id] = pokemon
            elif pokemon.cp > best_pokemon[pokemon_id].cp:
                best_pokemon[pokemon_id] = pokemon
        return best_pokemon

    def _transfer_pokemon(self, pokemon_list):
        requests = [make_request(Requests.RELEASE_POKEMON, params={
            'pokemon_id': pokemon.id
        }) for pokemon in pokemon_list]
        response = process_requests(self._rpc_client, requests)
        pass