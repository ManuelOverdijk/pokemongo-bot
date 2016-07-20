from requests import session
from random import randint
from settings import API_INITIAL_URL, API_USER_AGENT, PTC_TOKEN_MARKER
from protocol.Networking.Envelopes.RequestEnvelope_pb2 import RequestEnvelope
from protocol.Networking.Envelopes.ResponseEnvelope_pb2 import ResponseEnvelope
from protocol.Networking.Requests.Request_pb2 import Request
from protocol.Networking.Requests.RequestType_pb2 import GET_PLAYER
from protocol.Networking.Requests.Messages.GetPlayerMessage_pb2 import GetPlayerMessage


class RpcClient:
    token = None
    player = None
    _request_id = randint(1000000, 9999999)

    def __init__(self, token, player):
        self.token = token
        self.player = player
        self._session = session()
        self._session.headers.update({'User-Agent': API_USER_AGENT})
        self._api_url = API_INITIAL_URL
        self._api_auth_ticket = None

        self._api_url = self.get_own_api_url()

    def get_own_api_url(self):
        api_url = self.call(GET_PLAYER, GetPlayerMessage())
        pass

    def call(self, request_type, request_message):
        self._request_id += 1
        request_env = RequestEnvelope()
        request_env.request_id = self._request_id
        request_env.status_code = 2
        request_env.altitude = 0.0
        request_env.latitude = self.player.lat
        request_env.longitude = self.player.lon
        request_env.unknown12 = 123
        if not self._api_auth_ticket:
            request_env.auth_info.provider = 'ptc' if PTC_TOKEN_MARKER \
                                                  in self.token else 'google'
            request_env.auth_info.token.contents = self.token
            request_env.auth_info.token.unknown2 = 59
        else:
            request_env.auth_ticket = self._api_auth_ticket

        request = request_env.requests.add()
        request.request_type = request_type
        request.request_message = request_message.SerializeToString()

        result = self._session.post(self._api_url,
                                      data=request_env.SerializeToString())

        ## TODO: add result data to ResponseEnvelope,
        #  save auth_ticket from response locally,
        #  return resulting response envelope content


        pass
