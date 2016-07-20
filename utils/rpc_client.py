from requests import session
from random imxport randint
from settings import API_INITIAL_URL, API_OWN_URL, API_USER_AGENT

from POGOProtos.Networking.Envelopes_pb2 import (
    RequestEnvelope,
    ResponseEnvelope
)

from pgoexceptions import RpcException

class RpcClient(object):

    def __init__(self, player):
        self.player = player
        self.__request_id = randint(1000000, 9999999)
        self.__session = session()
        self.__session.headers.update({'User-Agent': API_USER_AGENT})
        self.__api_url = API_INITIAL_URL
        self.__api_auth_ticket = None

    def authenticate(self, login_session):
        if not login_session.is_logged_in:
            raise RpcException(
                'RpcClient.authenticate: not logged in'
            )

        if self.__api_auth_ticket:
            raise RpcException(
                'RpcClient.authenticate: already authenticated'
            )
        else:
            try:
                request_env = self.__prepare_request()
                request_env.auth_info.provider = login_session.provider
                request_env.auth_info.token.contents = login_session.auth_token
                request_env.auth_info.token.unknown2 = 59

                response = self.__call_rpc(requests = [], request_env = request_env)
                self.__api_auth_ticket = response.auth_ticket
            except:
                return False

            return True

    def call(self, requests):
        if not self.isauthenticated:
            raise RpcException(
                'RpcClient.call: not authenticated'
            )
        else:
            return self.__call_rpc(requests).returns

    def get_response(self, request, rpc_id, response_type):
        response_data = self.call([(request, rpc_id)])[0]
        return response_type.ParseFromString(response_data)

    def get_responses(self, request_list):
        requests = [(req, rpc_id) for req, rpc_id, _ in request_list]
        response_types = [resp for _, _, resp in request_list]

        response_data_list = self.call(requests)
        zipped_responses = zip(response_types, response_data_list)
        return [type.ParseFromString(data) for type, data in zipped_responses]

    @property
    def is_authenticated(self):
        return self.__api_auth_ticket is not None

    def __call_rpc(self, requests, request_env = None):
        self.__request_id += 1

        if not request_env:
            request_env = self.__prepare_request()
            request_env.auth_ticket.CopyFrom(self.__api_auth_ticket)

        for req_type, req_message in requests:
            request = request_env.requests.add()
            request.request_type = req_type
            request.request_message = req_message.SerializeToString()

        response_env = self.__get_response(request_env)
        # Every response envelope contains an api url, might as well update
        # every call.
        self.__api_url = API_OWN_URL.format(response_env.api_url)

        return response_env

    def __prepare_request(self):
        request_env = RequestEnvelope()
        request_env.request_id = self.__request_id
        request_env.status_code = 2
        request_env.altitude = 0.0
        request_env.latitude = self.player.lat
        request_env.longitude = self.player.lon
        request_env.unknown12 = 123
        return request_env

    def __get_response(self, envelope):
        result = self.__session.post(self.__api_url,
                                    data=envelope.SerializeToString())
        response = ResponseEnvelope()
        response.ParseFromString(result.content)
        return response
