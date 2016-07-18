class AuthProvider(object):
    """
    """

    def get_access_token(username, password):
        raise NotImplementedError(
        'AuthProvider.get_access_token is an abstract function')

class PTCAuthProvider(AuthProvider):

    def get_access_token(username, password):
        pass
