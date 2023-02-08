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


class Error6666666(Exception):
    def __init__(self,msg):
        self.msg = msg