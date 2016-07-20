from requests import session
from random import randint
from settings import API_INITIAL_URL, API_OWN_URL, API_USER_AGENT
from protocol.Networking.Envelopes.RequestEnvelope_pb2 import RequestEnvelope
from protocol.Networking.Envelopes.ResponseEnvelope_pb2 import ResponseEnvelope
from protocol.Networking.Requests.Request_pb2 import Request
from protocol.Networking.Requests.RequestType_pb2 import GET_PLAYER
from protocol.Networking.Requests.Messages.GetPlayerMessage_pb2 import GetPlayerMessage


class RpcClient:

    def __init__(self, player):
        self.player = player
        self._request_id = randint(1000000, 9999999)
        self._session = session()
        self._session.headers.update({'User-Agent': API_USER_AGENT})
        self._api_url = API_INITIAL_URL
        self._api_auth_ticket = None

    def authenticate(self, token, provider):
        if self._api_auth_ticket:
            raise AssertionError(
                'RpcClient.authenticate: already authenticated'
            )
        else:
            try:
                request_env = self._prepare_request()
                request_env.auth_info.provider = provider
                request_env.auth_info.token.contents = token
                request_env.auth_info.token.unknown2 = 59

                response = self.call(requests = [], request_env = request_env)
                self._api_auth_ticket = response.auth_ticket
            except:
                return False

            return True

    def call(self, requests, request_env = None):
        self._request_id += 1

        if not request_env:
            request_env = self._prepare_request()
            request_env.auth_ticket.CopyFrom(self._api_auth_ticket)

        for req_type, req_message in requests:
            request = request_env.requests.add()
            request.request_type = req_type
            request.request_message = req_message.SerializeToString()

        response_env = self._get_response(request_env)
        # Every response envelope contains an api url, might as well update
        # every call.
        self._api_url = API_OWN_URL.format(response_env.api_url)

        return response_env

    def _prepare_request(self):
        request_env = RequestEnvelope()
        request_env.request_id = self._request_id
        request_env.status_code = 2
        request_env.altitude = 0.0
        request_env.latitude = self.player.lat
        request_env.longitude = self.player.lon
        request_env.unknown12 = 123
        return request_env

    def _get_response(self, envelope):
        result = self._session.post(self._api_url,
                                    data=envelope.SerializeToString())
        response = ResponseEnvelope()
        response.ParseFromString(result.content)
        return response
