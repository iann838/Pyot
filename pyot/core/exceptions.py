from typing import Mapping


class NotFindable(Exception):
    def __init__(self):
        Exception.__init__(self, "[Trace: Pyot Pipeline] 600: Pipeline token matching pair not found")


class SessionNotFound(Exception):
    def __init__(self, origin="Non Pyot Source Origin"):
        Exception.__init__(self, f"[Trace: Pyot Pipeline] 601: Session Not Found. Origin: {origin}")


class DecodeError(Exception):
    def __init__(self, origin="Non Pyot Source Origin"):
        Exception.__init__(self, f"[Trace: Pyot Pipeline] 602: AioHttp took too long to decode the response. Origin: {origin}")


class NoContent(Exception):
    def __init__(self, origin="Non Pyot Source Origin"):
        Exception.__init__(self, f"[Trace: Pyot Pipeline] 204: No Content. Origin: {origin}")


class NotFound(Exception):
    def __init__(self, origin="Non Pyot Source Origin"):
        Exception.__init__(self, f"[Trace: Pyot Pipeline] 404: Data Not Found. Origin: {origin}")


class MethodNotAllowed(Exception):
    def __init__(self, origin="Non Pyot Source Origin"):
        Exception.__init__(self, f"[Trace: Pyot Pipeline] 405: Method Not Allowed. Origin: {origin}")


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


