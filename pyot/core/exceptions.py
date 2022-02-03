from typing import Mapping


class PyotException(Exception):
    code: int


class NotFindable(PyotException):

    code = 600

    def __init__(self):
        PyotException.__init__(self, "[600] Pipeline token matching pair not found")


class SessionNotFound(PyotException):

    code = 601

    def __init__(self, origin="Unknown"):
        PyotException.__init__(self, f"[601] Session Not Found. Origin: {origin}")


class DecodeError(PyotException):

    code = 602

    def __init__(self, origin="Unknown"):
        PyotException.__init__(self, f"[602] AioHttp took too long to decode the response. Origin: {origin}")


class NoContent(PyotException):

    code = 204

    def __init__(self, origin="Unknown"):
        PyotException.__init__(self, f"[204] No Content. Origin: {origin}")


class NotFound(PyotException):

    code = 404

    def __init__(self, origin="Unknown"):
        PyotException.__init__(self, f"[404] Data Not Found. Origin: {origin}")


class MethodNotAllowed(PyotException):

    code = 405

    def __init__(self, origin="Unknown"):
        PyotException.__init__(self, f"[405] Method Not Allowed. Origin: {origin}")


class ServerError(PyotException):
    messages: Mapping[int, str] = {
        500: "Internal Server Error",
        502: "Bad Gateway",
        503: "Service Unavailable",
        504: "Gateway Timeout",
    }

    def __init__(self, code, origin="Unknown"):
        self.code = code
        PyotException.__init__(self, f"[{code}] {self.messages[code]}. Origin: {origin}")


class RateLimited(PyotException):

    code = 429

    def __init__(self, origin="Unknown"):
        PyotException.__init__(self, f"[429] Rate limit Exceeded. Origin: {origin}")


class Forbidden(PyotException):

    code = 403

    def __init__(self, origin="Unknown"):
        PyotException.__init__(self, f"[403] Access Forbidden. Origin: {origin}")


class Unauthorized(PyotException):

    code = 401

    def __init__(self, origin="Unknown"):
        PyotException.__init__(self, f"[401] Access Unauthorized. Origin: {origin}")


class BadRequest(PyotException):

    code = 400

    def __init__(self, origin="Unknown"):
        PyotException.__init__(self, f"[400] Bad Request. Origin: {origin}")


class Timeout(PyotException):

    code = 408

    def __init__(self, origin="Unknown"):
        PyotException.__init__(self, f"[408] Timeout Connection. Origin: {origin}")


class UnidentifiedResponse(PyotException):

    def __init__(self, code, origin="Unknown"):
        self.code = code
        PyotException.__init__(self, f"[{code}] Unidentified Response {code}. Origin: {origin}")
