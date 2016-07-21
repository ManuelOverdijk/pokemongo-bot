__request_processors = {}
__response_processors = {}

def __register_request(request_type, response_type, rpc_id, request_handler):
    __request_processors[request_type] = (
        response_type, rpc_id, request_handler)


def __register_response(response_type, response_handler):
    __response_processors[response_type] = response_handler


def request_processor(request_type, response_type, rpc_id):
    def decorator(function):
        def wrapper(*args, **kwargs):
            return function(*args, **kwargs)
        __register_request(request_type, response_type, rpc_id, wrapper)
        return wrapper
    return decorator


def response_processor(response_type):
    def decorator(function):
        def wrapper(player, data, response):
            return function(player=player, data=data, response=response)
        __register_response(response_type, wrapper)
        return wrapper
    return decorator
