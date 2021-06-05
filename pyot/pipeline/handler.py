import asyncio
from typing import Dict
import copy

from pyot.core import exceptions as exc


class ErrorHandler:

    DEFAULT_HANDLER = {
        204 : ("T", []),
        400 : ("T", []),
        401 : ("T", []),
        404 : ("T", []),
        403 : ("T", []),
        405 : ("T", []),
        408 : ("E", [3, 3]),
        429 : ("E", [3, 3]),
        500 : ("E", [3, 3]),
        502 : ("E", [3, 3]),
        503 : ("E", [3, 3]),
        504 : ("E", [3, 3]),
        602 : ("R", [2]),
        800 : ("T", []),
    }

    def __init__(self, handler: Dict, on_key_error: int = 800) -> None:
        self.handler = copy.deepcopy(self.DEFAULT_HANDLER)
        self.on_key_error = on_key_error
        if handler is None:
            return
        self.validate_handler(handler)
        self.handler.update(handler)

    def __getitem__(self, code: int):
        try:
            return self.handler[code]
        except KeyError:
            return self.handler[self.on_key_error]

    def validate_handler(self, handler: Dict):
        for code, c in handler.items():
            if code not in self.DEFAULT_HANDLER:
                raise RuntimeError(f"Handler code {code} is not a valid status for error handling")
            strategy = c[0]
            try:
                params = c[1]
            except IndexError as e:
                raise AttributeError("Handler values receives 2 paramameters, 1 was given") from e
            for a in params:
                if not isinstance(a, int):
                    raise RuntimeError(f"Handler strategy takes 'int' parameters, '{type(a)}' was given")
            if strategy == "T":
                if len(params) != 0:
                    raise RuntimeError(f"Handler strategy 'T' (Throw) takes 0 parameters, but {len(params)} was given")
            elif strategy == "E":
                if len(params) != 2:
                    raise RuntimeError(f"Handler strategy 'E' (Exp. backoff) takes 2 parameters, but {len(params)} was given")
            elif strategy == "R":
                if len(params) != 1:
                    raise RuntimeError(f"Handler strategy 'R' (Retry) takes 1 parameters, but {len(params)} was given")
            else:
                raise RuntimeError(f"Handler strategy '{strategy}' is not a valid token for error handling")

    def get_token(self) -> "ErrorToken":
        return ErrorToken(self)


class ErrorToken:

    def __init__(self, instance: ErrorHandler, tries: int = 0, raise_at: int = 1, exception: Exception = None, code: int = 0) -> None:
        self.instance = instance
        self.tries = tries
        self.raise_at = raise_at
        self.exception = exception
        self.code = code

    async def consume(self, code: int, origin: str):
        how = self.instance[code]
        strategy = how[0]
        params = how[1]

        if self.code != code:
            self.exception = None
            self.code = code

        if self.exception is None:
            if code == 404:
                self.exception = exc.NotFound(origin)
            elif code == 204:
                self.exception = exc.NoContent(origin)
            elif code in [500, 502, 503, 504]:
                self.exception = exc.ServerError(code, origin)
            elif code == 429:
                self.exception = exc.RateLimited(origin)
            elif code == 403:
                self.exception = exc.Forbidden(origin)
            elif code == 405:
                self.exception = exc.MethodNotAllowed(origin)
            elif code == 401:
                self.exception = exc.Unauthorized(origin)
            elif code == 400:
                self.exception = exc.BadRequest(origin)
            elif code == 408:
                self.exception = exc.Timeout(origin)
            elif code == 602:
                self.exception = exc.DecodeError(origin)
            elif code == 601:
                self.exception = exc.SessionNotFound(origin)
            elif code == 600:
                self.exception = exc.NotFindable()
            elif code == 800:
                self.exception = exc.UnidentifiedResponse(code, origin)
            else:
                self.exception = Exception("Unexpected error. Please open an issue on github repository")

            if strategy != "T":
                self.raise_at = params[-1]+1
            else:
                self.raise_at = 1

        self.tries += 1
        if strategy == "E" and self.tries < self.raise_at:
            await asyncio.sleep(params[0]**self.tries)

    def allow(self):
        if self.tries < self.raise_at:
            return True
        raise self.exception
