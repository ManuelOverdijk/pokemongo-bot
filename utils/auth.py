import json
import re

import requests

import settings


class PtcAuth(object):
    LOGIN_HEADERS = {
        'user-agent': settings.LOGIN_USER_AGENT
    }

    def __init__(self):
        self._session = self._make_session()

    def get_auth_token(self, username, password):
        login_data = self._get_login_data()
        login_token = self._get_login_token(username, password, login_data)

        return self._get_oauth_token(login_token)

    def _get_login_data(self):
        response = self._session.get(settings.PTC_LOGIN_URL)
        return json.loads(response.content)

    def _get_login_token(self, username, password, login_data):
        payload = self._make_login_payload(username, password, login_data)
        response = self._session.post(settings.PTC_LOGIN_URL,
                                      data=payload,
                                      allow_redirects=False)

        token_found = False
        try:
            jsonresponse = response.json()
        except ValueError:
            token_found = True

        if token_found:
            token_data = response.headers['location']
            return token_data[token_data.rfind('=') + 1:]

        raise ValueError(
            'token not found: {0}'.format(str(jsonresponse['errors']))
        )

    def _get_oauth_token(self, login_token):
        payload = self._make_oauth_payload(login_token)
        response = self._session.post(settings.PTC_OAUTH_URL, data=payload)

        token = re.sub('.*en=', '', response.content)
        return re.sub('.com.*', '.com', token)

    def _make_login_payload(self, username, password, login_tokens):
        return {
            'lt': login_tokens['lt'],
            'execution': login_tokens['execution'],
            '_eventId': 'submit',
            'username': username,
            'password': password
        }

    def _make_oauth_payload(self, token):
        return {
            'client_id': settings.PTC_CLIENT_ID,
            'redirect_uri': settings.PTC_CLIENT_REDIRECT_URI,
            'client_secret': settings.PTC_CLIENT_SECRET,
            'grant_type': 'refresh_token',
            'code': token
        }

    def _make_session(self):
        session = requests.session()
        session.headers.update(self.LOGIN_HEADERS)

        return session
