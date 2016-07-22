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
    # Returns just the response object, and not the RPC id.
    # This is because looking for the matching response is not needed
    # when only a single request was made.
    request_id = request[0]
    response = process_requests(rpc, [request])
    if response:
        return response[request_id]

    return None

def process_requests(rpc, requests):
    messages = rpc.get_responses(requests)
    zipped_requests = zip(requests, messages)
    responses = {}
    if any(zipped_requests):
        for request, response_data in zipped_requests:
            request_type = request[0]
            response_class = request_processors[request_type][0]
            response_object = response_class()
            response_object.ParseFromString(response_data)
            responses[request_type] = response_object

    return responses
