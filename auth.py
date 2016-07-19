import requests
import settings
import re
import json

class PTCAuth(object):

    LOGIN_HEADERS = {
        'user-agent': settings.LOGIN_USER_AGENT
    }

    def __init__(self):
        self._session = self._make_session()

    def get_auth_ticket(self, username, password):
        login_data = self._get_login_data()
        login_ticket = self._get_login_ticket(username, password, login_data)

        return self._get_oauth_ticket(login_ticket)

    def _get_login_data(self):
        response = self._session.get(settings.PTC_LOGIN_URL)
        return json.loads(response.content)

    def _get_login_ticket(self, username, password, login_data):
        payload = self._make_login_payload(username, password, login_data)
        response = self._session.post(settings.PTC_LOGIN_URL,
                                     data=payload,
                                     allow_redirects=False)

        ticket_found = False
        try:
            jsonresponse = response.json()
        except ValueError:
            ticket_found = True

        if ticket_found:
            ticket_data = response.headers['location']
            return ticket_data[ticket_data.rfind('=') + 1:]

        raise ValueError(
            'Ticket not found: {0}'.format(str(jsonresponse['errors']))
        )

    def _get_oauth_ticket(self, login_ticket):
        payload = self._make_oauth_payload(login_ticket)
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

    def _make_oauth_payload(self, ticket):
        return {
            'client_id': settings.PTC_CLIENT_ID,
            'redirect_uri': settings.PTC_CLIENT_REDIRECT_URI,
            'client_secret': settings.PTC_CLIENT_SECRET,
            'grant_type': 'refresh_token',
            'code': ticket
        }

    def _make_session(self):
        session = requests.session()
        session.headers.update(self.LOGIN_HEADERS)

        return session
