from typing import Mapping


class SessionNotFound(Exception):
    def __init__(self):
        Exception.__init__(self, "[Trace: Pyot Pipeline] 661: Session Not Found, use 'pyot.run' to your coroutines")


class NotFound(Exception):
    def __init__(self):
        Exception.__init__(self, "[Trace: Pyot Pipeline] 404: Data Not Found")
        
        
class ServerError(Exception):
    messages: Mapping[int, str] = {
        500: "Internal Server Error",
        502: "Bad Gateway",
        503: "Service Unavailable",
        504: "Gateway Timeout",

    }
    def __init__(self, code):
        Exception.__init__(self, f"[Trace: Pyot Pipeline] {code}: {self.messages[code]}")
        

class RateLimited(Exception):
    def __init__(self):
        Exception.__init__(self, "[Trace: Pyot Pipeline] 429: Rate limit Exceeded")


class Forbidden(Exception):
    def __init__(self):
        Exception.__init__(self, "[Trace: Pyot Pipeline] 403: Access Forbidden")


class Unauthorized(Exception):
    def __init__(self):
        Exception.__init__(self, "[Trace: Pyot Pipeline] 401: Access Unauthorized")


class BadRequest(Exception):
    def __init__(self,):
        Exception.__init__(self, "[Trace: Pyot Pipeline] 400: Bad Request")


class Timeout(Exception):
    def __init__(self):
        Exception.__init__(self, "[Trace: Pyot Pipeline] 408: Timeout Connection")


class UnidentifiedResponse(Exception):
    def __init__(self, code):
        Exception.__init__(self, f"[Trace: Pyot Pipeline] {code}: Unidentified Response {code}")


