from random import randint
from requests import session
from POGOProtos.Networking.Envelopes_pb2 import (
    RequestEnvelope,
    ResponseEnvelope
)
from pgoexceptions import RpcException
from settings import API_INITIAL_URL, API_OWN_URL, API_USER_AGENT


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

        if self.is_authenticated:
            raise RpcException(
                'RpcClient.authenticate: already authenticated'
            )
        else:
            try:
                request_env = self.__prepare_request()
                request_env.auth_info.provider = login_session.provider
                request_env.auth_info.token.contents = login_session.auth_token
                request_env.auth_info.token.unknown2 = 59

                response = self.__call_rpc(requests=[],
                                           request_env=request_env)
                self.__api_auth_ticket = response.auth_ticket
            except:
                return False

            return True

    def get_response(self, request):
        try:
            return self.get_responses([request])[0]
        except IndexError:
            return None

    def get_responses(self, requests):
        if not self.is_authenticated:
            raise RpcException(
                'RpcClient.call: not authenticated'
            )
        else:
            return self.__call_rpc(requests).returns

    @property
    def is_authenticated(self):
        return self.__api_auth_ticket is not None

    def __call_rpc(self, requests, request_env=None):
        self.__request_id += 1

        if not request_env:
            request_env = self.__prepare_request()
            request_env.auth_ticket.CopyFrom(self.__api_auth_ticket)

        for req_type, req_message in requests:
            request = request_env.requests.add()
            request.request_type = req_type
            request.request_message = req_message.SerializeToString()

        response_env = self.__get_response(request_env)
        try:
            if response_env.api_url:
                api_url = response_env.api_url
                self.__api_url = API_OWN_URL.format(api_url)
        except:
            pass

        return response_env

    def __prepare_request(self):
        request_env = RequestEnvelope()
        request_env.request_id = self.__request_id
        request_env.status_code = 2
        request_env.altitude = self.player.alt
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
