from typing import Any, Dict, Tuple
from dataclasses import dataclass
from pyot.core import exceptions as exc
import asyncio


@dataclass
class RequestToken:
    _tries: int = 0
    _raise_at: int = 1
    _exception: Any = None
    _code: int = 0

    async def stream(self, code: int, how: Tuple, origin: str):
        strategy = how[0]
        params = how[1]
        if self._code != code:
            self._exception = None
            self._code = code

        if self._exception is None:
            if code == 404:
                self._exception = exc.NotFound(origin)
            elif code == 204:
                self._exception = exc.NoContent(origin)
            elif code in [500, 502, 503, 504]:
                self._exception = exc.ServerError(code, origin)
            elif code == 429:
                self._exception = exc.RateLimited(origin)
            elif code == 403:
                self._exception = exc.Forbidden(origin)
            elif code == 405:
                self._exception = exc.MethodNotAllowed(origin)
            elif code == 401:
                self._exception = exc.Unauthorized(origin)
            elif code == 400:
                self._exception = exc.BadRequest(origin)
            elif code == 408:
                self._exception = exc.Timeout(origin)
            elif code == 602:
                self._exception = exc.DecodeError(origin)
            elif code == 800:
                self._exception = exc.UnidentifiedResponse(code, origin)
            else:
                self._exception = Exception("Unexpected error. Please contact Pyot Dev")

            if strategy != "T":
                self._raise_at = params[-1]+1
            else:
                self._raise_at = 1
        
        self._tries += 1
        if strategy == "E" and self._tries < self._raise_at:
            await asyncio.sleep(params[0]**self._tries)

    async def run_or_raise(self):
        if self._tries < self._raise_at:
            return True
        else:
            raise self._exception


@dataclass
class PipelineToken:
    model: str
    server: str
    method: str
    params: Dict[str, Any]
    queries: Dict[str, Any]

    def __hash__(self):
        return hash((self.model, self.server, self.method, str(self.params), str(self.queries)))

    @property
    def stringify(self):
        return (self.model+self.server+self.method+str(self.params)+str(self.queries)).replace(" ", "_")
