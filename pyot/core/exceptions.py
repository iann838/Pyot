from typing import Mapping


class PyotException(Exception):
    pass


class NotFindable(PyotException):
    def __init__(self):
        PyotException.__init__(self, "[Trace: Pyot Pipeline] 600: Pipeline token matching pair not found")


class SessionNotFound(PyotException):
    def __init__(self, origin="Non Service Origin"):
        PyotException.__init__(self, f"[Trace: Pyot Pipeline] 601: Session Not Found. Origin: {origin}")


class DecodeError(PyotException):
    def __init__(self, origin="Non Service Origin"):
        PyotException.__init__(self, f"[Trace: Pyot Pipeline] 602: AioHttp took too long to decode the response. Origin: {origin}")


class NoContent(PyotException):
    def __init__(self, origin="Non Service Origin"):
        PyotException.__init__(self, f"[Trace: Pyot Pipeline] 204: No Content. Origin: {origin}")


class NotFound(PyotException):
    def __init__(self, origin="Non Service Origin"):
        PyotException.__init__(self, f"[Trace: Pyot Pipeline] 404: Data Not Found. Origin: {origin}")


class MethodNotAllowed(PyotException):
    def __init__(self, origin="Non Service Origin"):
        PyotException.__init__(self, f"[Trace: Pyot Pipeline] 405: Method Not Allowed. Origin: {origin}")


class ServerError(PyotException):
    messages: Mapping[int, str] = {
        500: "Internal Server Error",
        502: "Bad Gateway",
        503: "Service Unavailable",
        504: "Gateway Timeout",

    }
    def __init__(self, code, origin="Non Service Origin"):
        PyotException.__init__(self, f"[Trace: Pyot Pipeline] {code}: {self.messages[code]}. Origin: {origin}")


class RateLimited(PyotException):
    def __init__(self, origin="Non Service Origin"):
        PyotException.__init__(self, f"[Trace: Pyot Pipeline] 429: Rate limit Exceeded. Origin: {origin}")


class Forbidden(PyotException):
    def __init__(self, origin="Non Service Origin"):
        PyotException.__init__(self, f"[Trace: Pyot Pipeline] 403: Access Forbidden. Origin: {origin}")


class Unauthorized(PyotException):
    def __init__(self, origin="Non Service Origin"):
        PyotException.__init__(self, f"[Trace: Pyot Pipeline] 401: Access Unauthorized. Origin: {origin}")


class BadRequest(PyotException):
    def __init__(self, origin="Non Service Origin"):
        PyotException.__init__(self, f"[Trace: Pyot Pipeline] 400: Bad Request. Origin: {origin}")


class Timeout(PyotException):
    def __init__(self, origin="Non Service Origin"):
        PyotException.__init__(self, f"[Trace: Pyot Pipeline] 408: Timeout Connection. Origin: {origin}")


class UnidentifiedResponse(PyotException):
    def __init__(self, code, origin="Non Service Origin"):
        PyotException.__init__(self, f"[Trace: Pyot Pipeline] {code}: Unidentified Response {code}. Origin: {origin}")
