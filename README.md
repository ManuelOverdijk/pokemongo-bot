# pokemongo-bot
A modular bot for Pokémon GO written in Python. Easy to extend, highly dev-able. 

Leans heavily on [AeonLucid's Protobuf work](https://github.com/AeonLucid/POGOProtos), and a bit of [Mila432's API](https://github.com/Mila432/Pokemon_Go_API).

###Current features and plans:
- [x] A priority-based module system that makes it easy to add new behaviour
- [x] A task scheduler that controls which modules get the control flow
- [x] Configurable fast teleportation or actual human-like walking
- [x] Farming of Pokémon with maximum XP bonuses
- [x] Searching of PokéStops
- [x] Automatic transferral of the weakest CP Pokémon of each type
- [ ] Evolving of the strongest CP Pokémon of each type
- [ ] Automatic removal of unwanted items from the inventory
- [ ] Automatic usage of lucky eggs to gain XP boosts

###Installation:
- Install [Google's 'protoc' tool](https://github.com/google/protobuf/releases/download/v3.0.0-beta-3.1/protoc-3.0.0-beta-3.1-osx-x86_64.zip), at version 3+ (Download files and copy to a $PATH dir)
- Pip install the requirements (pip install -r requirements.txt --user python)
- `bash scripts/compile_proto.sh`

###Running
- `python main.py`

## Credits
* https://github.com/AeonLucid/POGOProtos
* https://github.com/Mila432/Pokemon_Go_API
* https://github.com/tejado/pokemongo-api-demo
