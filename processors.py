from utils.processor_helper import (
    register_request,
    regisetered_request,
    build_request,
    request_processors
)
# PROCESSOR USAGE EXAMPLE
# params = {'encounter_id': encounter_id, 'spawnpoint_id': spawnpoint_id}
# request = make_request(EncounterMessage, player, data, params=params)
# answer = process_request(rpc, request)
# if not answer:
#    print 'Encounter failed!'
# else:
#    print 'Encounter successful!'


def make_request(request_type, params={}):
    if not regisetered_request(request_type):
        register_request(request_type)
    return build_request(request_type, params)


def process_request(rpc, request):
    return process_requests(rpc, [request])

def process_requests(rpc, requests):
    messages = []
    for request_type, request in requests:
        response_type, _ = request_processors[request_type]
        messages.append((request, request_type, response_type))
    return rpc.get_responses(messages)
