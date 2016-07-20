
class AuthenticationException(Exception):
    def __init__(self, message):
        super(self.__class__, self).__init__(message)

class RPCException(Exception):
    def __init__(self, message):
        super(self.__class__, self).__init__(message)
