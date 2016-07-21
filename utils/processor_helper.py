from collections import Iterable
from importlib import import_module

from POGOProtos.Networking.Requests_pb2 import RequestType

request_processors = {}


def register_request(request_type):
    if not __is_valid_type(request_type):
        raise AttributeError(
            'processor_helper.register_request: request id %d not defined in protocol' % request_type
        )
    request_class = __get_request_class(request_type)
    response_class = __gett_response_class(request_type)
    request_handler = __request_processor(request_class)
    request_processors[request_type] = (response_class, request_handler)


def regisetered_request(request_type):
    return request_type in request_processors


def build_request(request_type, params={}):
    if not regisetered_request(request_type):
        raise AttributeError(
            'processor_helper.invoke_request: request %s not registered' % RequestType.Name(
                request_type)
        )
    _, request_handler = request_processors[request_type]
    return (request_type, request_handler(**params))


def __request_processor(request_class):
    def wrapper(**kwargs):
        obj = request_class()
        for k, v in kwargs.iteritems():
            if isinstance(v, Iterable) and not isinstance(v, basestring):
                getattr(obj, k).extend(v)
            else:
                setattr(obj, k, v)
        return obj

    return wrapper


def __is_valid_type(request_type):
    try:
        name = RequestType.Name(request_type)
        return True if name else False
    except:
        return False


def __get_request_class(request_type):
    reqname = __request_name(request_type)
    lib = import_module('POGOProtos.Networking.Requests.Messages_pb2')
    return getattr(lib, reqname)


def __gett_response_class(request_type):
    respname = __response_name(request_type)
    lib = import_module('POGOProtos.Networking.Responses_pb2')
    return getattr(lib, respname)


def __request_name(request_type):
    cam_name = __camel_case_request_name(request_type)
    return cam_name + 'Message'


def __response_name(request_type):
    cam_name = __camel_case_request_name(request_type)
    return cam_name + 'Response'


def __camel_case_request_name(request_type):
    name = RequestType.Name(request_type)
    name.lower()
    return ''.join([i.capitalize() for i in name.split('_') if i])
