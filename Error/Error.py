class CookieFailedError(Exception):
    def __init__(self, msg):
        self.msg = msg


class StatusCodeError(Exception):
    def __init__(self, msg):
        self.msg = msg


class FuncNotExistsError(Exception):
    def __init__(self, msg):
        self.msg = msg


class SizeNotExistsError(Exception):
    def __init__(self, msg):
        self.msg = msg


class ContentNotExistsError(Exception):
    def __init__(self, msg):
        self.msg = msg


class ParamsError(Exception):
    def __init__(self, msg):
        self.msg = msg


class ServerError(Exception):
    def __init__(self, msg):
        self.msg = msg


class ServiceUnavailableError(Exception):
    def __init__(self, msg):
        self.msg = msg
