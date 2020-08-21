from datetime import timedelta as td
from dataclasses import dataclass
from typing import Tuple, Any
from ..core import exceptions as exc
from ..core.core import run
import asyncio
import aiohttp
import atexit


class PyotStoreObject:

    def _log_template(self, token):
        return f"<{token.server.upper()} {token.method}: {' '.join([str(token.params[k]) for k in token.params])}>"

    async def initialize(self):
        raise NotImplementedError

    async def get(self, token):
        raise NotImplementedError

    async def put(self, token, response):
        raise NotImplementedError

    async def clear(self):
        raise NotImplementedError

    async def expire(self):
        raise NotImplementedError
    
    async def delete(self, token):
        raise NotImplementedError

    async def contains(self, token):
        raise NotImplementedError


class PyotExpirationManager:
    _expirations = {
        "lol": {
            "champion-v3-rotation": td(hours=3),
            "champion-mastery-v4-all-mastery": td(minutes=30),
            "champion-mastery-v4-by-champion-id": td(minutes=30),
            "clash-v1-players": td(minutes=5),
            "clash-v1-teams": td(minutes=5),
            "clash-v1-tournaments-by-team-id": td(minutes=5),
            "clash-v1-toutnaments-by-tournament-id": td(minutes=5),
            "clash-v1-tournaments-all": td(hours=3),
            "league-v4-summoner-entries": td(hours=3),
            "league-v4-challenger-league": td(hours=1),
            "league-v4-grandmaster-league": td(hours=1),
            "league-v4-master-league": td(hours=1),
            "league-v4-entries-by-division": td(hours=1),
            "league-v4-league-by-league-id": td(hours=1),
            "status-v3-shard-data": td(minutes=5),
            "match-v4-match": td(days=7),
            "match-v4-timeline": td(days=3),
            "match-v4-matchlist": td(minutes=5),
            "spectator-v4-current-game": td(minutes=5),
            "spectator-v4-featured-games": td(minutes=5),
            "summoner-v4-by-name": td(hours=3),
            "summoner-v4-by-id": td(hours=3),
            "summoner-v4-by-account-id": td(hours=3),
            "summoner-v4-by-puuid": td(hours=3),
            "third-party-code-v4-code": 0,
        },
        "val": {
            "account-v1-by-puuid": td(hours=3),
            "account-v1-by-riot-id": td(hours=3),
            "account-v1-active-shard": td(hours=3),
            "match-v1-match": td(days=7),
            "match-v1-matchlist": td(minutes=5),
            "content-v1-contents": td(hours=3),
        }
    }

    def __init__(self, game, custom_expirations):
        if custom_expirations is not None:
            self._expirations[game].update(custom_expirations)
        expire = self._expirations[game]
        self.expirations = self._create_expiration(expire)

    def _create_expiration(self, expirations):
        expirations_ = {}
        for key, time in expirations.items():
            if type(time) is td:
                expirations_[key] = time.total_seconds()
            else:
                expirations_[key] = time
            if type(expirations_[key]) is not int and type(expirations_[key]) is not float:
                raise AttributeError(f"Expiration value not allowed, {type(expirations_[key])} was given")
        return expirations_
        
    def get_timeout(self, key):
        return self.expirations[key]


@dataclass
class PyotRequestToken:
    _tries: int = 0
    _raise_at: int = 1
    _exception: Any = None

    async def stream(self, code: int, how: Tuple):
        strategy = how[0]
        params = how[1]

        if self._exception is None:
            if code == 404:
                self._exception = exc.NotFound()
            elif code in [500, 502, 503, 504]:
                self._exception = exc.ServerError(code)
            elif code == 429:
                self._exception = exc.RateLimited()
            elif code == 403:
                self._exception = exc.Forbidden()
            elif code == 401:
                self._exception = exc.Unauthorized()
            elif code == 400:
                self._exception = exc.BadRequest()
            elif code == 408:
                self._exception = exc.Timeout()
            elif code == 888:
                self._exception = exc.UnidentifiedResponse(code)
            else:
                self._exception = Exception("Unexpected error. Please contact Pyot Dev")

            if strategy != "T":
                self._raise_at = params[-1]+1
        
        self._tries += 1
        if strategy == "E":
            await asyncio.sleep(params[0]**self._tries)

    async def run_or_raise(self):
        if self._tries < self._raise_at:
            return True
        else:
            raise self._exception


class PyotErrorHandler:
    default_handler = {
        400 : ("T", []),
        401 : ("T", []),
        404 : ("T", []),
        403 : ("T", []),
        408 : ("E", [3, 3]),
        429 : ("E", [3, 3]),
        500 : ("E", [3, 3]),
        502 : ("R", [3]),
        503 : ("E", [3, 3]),
        504 : ("R", [3]),
        888 : ("T", []),
    }

    def create_handler(self, handler):
        if handler is None:
            return self.default_handler
        for code, c in handler.items():
            if code not in self.default_handler.keys():
                raise RuntimeError(f"Handler code {code} is not a valid status for error handling")
            strategy = c[0]
            try:
                params = c[1]
            except IndexError:
                raise AttributeError("Handler values receives 2 paramameters, 1 was given")
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
        self.default_handler.update(handler)
        return self.default_handler