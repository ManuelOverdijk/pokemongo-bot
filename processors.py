from POGOProtos.Networking.Requests.Messages_pb2 import (
    EncounterMessage
)
from POGOProtos.Networking.Responses_pb2 import (
    EncounterResponse
)
from utils.processor_helper import *
import POGOProtos.Networking.Requests_pb2 as Requests

# PROCESSOR USAGE EXAMPLE
# params = {'encounter_id': encounter_id, 'spawnpoint_id': spawnpoint_id}
# request = make_request(EncounterMessage, player, data, params=params)
# answer = process_request(rpc, request)
# if not answer:
#    print 'Encounter failed!'
# else:
#    print 'Encounter successful!'

@request_processor(EncounterMessage, EncounterResponse, Requests.ENCOUNTER)
def encounter_message(player, data, encounter_id, spawnpoint_id):
    encounter = EncounterMessage()
    encounter.encounter_id = encounter_id
    encounter.spawnpoint_id = spawnpoint_id
    encounter.player_latitude = player.lat
    encounter.player_longitude = player.lon

    return encounter


@response_processor(EncounterResponse)
def encounter_response(player, data, response):
    # TODO: Update data and player
    pass


def make_request(request_type, player, data, params={}):
    return (request_type, player, data, params)


def process_request(rpc, made_request):
    return process_requests(rpc, [made_request])


def process_requests(rpc, requests):
    messages = []
    arguments = []

    for request, player, data, params in requests:
        args = {'player': player, 'data': data}
        response_args = dict(args)

        args.update(params)
        response_type, rpc_id, handler = __request_processors[request]

        messages.append((handler(**args), rpc_id, response_type))
        arguments.append(response_args)

    responses = zip(rpc.get_responses(messages), arguments)
    for response, arguments in responses:
        arguments['response'] = response
        __response_processors[response](**arguments)
