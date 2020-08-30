from typing import Mapping


class SessionNotFound(Exception):
    def __init__(self, origin="Non Pyot Source Origin"):
        Exception.__init__(self, f"[Trace: Pyot Pipeline] 661: Session Not Found, use 'pyot.run' to your coroutines. Origin: {origin}")


class NotFound(Exception):
    def __init__(self, origin="Non Pyot Source Origin"):
        Exception.__init__(self, f"[Trace: Pyot Pipeline] 404: Data Not Found. Origin: {origin}")
        
        
class ServerError(Exception):
    messages: Mapping[int, str] = {
        500: "Internal Server Error",
        502: "Bad Gateway",
        503: "Service Unavailable",
        504: "Gateway Timeout",

    }
    def __init__(self, code, origin="Non Pyot Source Origin"):
        Exception.__init__(self, f"[Trace: Pyot Pipeline] {code}: {self.messages[code]}. Origin: {origin}")
        

class RateLimited(Exception):
    def __init__(self, origin="Non Pyot Source Origin"):
        Exception.__init__(self, f"[Trace: Pyot Pipeline] 429: Rate limit Exceeded. Origin: {origin}")


class Forbidden(Exception):
    def __init__(self, origin="Non Pyot Source Origin"):
        Exception.__init__(self, f"[Trace: Pyot Pipeline] 403: Access Forbidden. Origin: {origin}")


class Unauthorized(Exception):
    def __init__(self, origin="Non Pyot Source Origin"):
        Exception.__init__(self, f"[Trace: Pyot Pipeline] 401: Access Unauthorized. Origin: {origin}")


class BadRequest(Exception):
    def __init__(self, origin="Non Pyot Source Origin"):
        Exception.__init__(self, f"[Trace: Pyot Pipeline] 400: Bad Request. Origin: {origin}")


class Timeout(Exception):
    def __init__(self, origin="Non Pyot Source Origin"):
        Exception.__init__(self, f"[Trace: Pyot Pipeline] 408: Timeout Connection. Origin: {origin}")


class UnidentifiedResponse(Exception):
    def __init__(self, code, origin="Non Pyot Source Origin"):
        Exception.__init__(self, f"[Trace: Pyot Pipeline] {code}: Unidentified Response {code}. Origin: {origin}")


