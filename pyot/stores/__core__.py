from datetime import timedelta as td
from dataclasses import dataclass
from typing import Tuple, Any, Dict
from ..core import exceptions as exc
import asyncio
import aiohttp
import atexit
import copy

from logging import getLogger
LOGGER = getLogger(__name__)

class PyotStoreObject:

    def _log_template(self, token):
        return f"<{token.server.upper()} {token.method}: {' '.join([str(token.params[k]) for k in token.params])}>"

    async def initialize(self):
        return True

    async def transform_key(self, *args):
        raise NotImplementedError

    async def get(self, token, *args):
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
            "account_v1_by_puuid": td(hours=3),
            "account_v1_active_shard": 0,
            "champion_v3_rotation": td(hours=3),
            "champion_mastery_v4_all_mastery": 0,
            "champion_mastery_v4_by_champion_id": 0,
            "clash_v1_players": 0,
            "clash_v1_teams": 0,
            "clash_v1_tournaments_by_team_id": 0,
            "clash_v1_toutnaments_by_tournament_id": 0,
            "clash_v1_tournaments_all": td(hours=3),
            "league_v4_summoner_entries": 0,
            "league_v4_challenger_league": td(hours=1),
            "league_v4_grandmaster_league": td(hours=1),
            "league_v4_master_league": td(hours=1),
            "league_v4_entries_by_division": 0,
            "league_v4_league_by_league_id": 0,
            "status_v3_shard_data": 0,
            "match_v4_match": td(days=7),
            "match_v4_timeline": td(days=3),
            "match_v4_matchlist": 0,
            "spectator_v4_current_game": 0,
            "spectator_v4_featured_games": 0,
            "summoner_v4_by_name": td(hours=1),
            "summoner_v4_by_id": td(hours=1),
            "summoner_v4_by_account_id": td(hours=1),
            "summoner_v4_by_puuid": td(hours=1),
            "third_party_code_v4_code": 0,

            "cdragon_champion_by_id": td(hours=1),
            "cdragon_item_full": td(hours=1),
            "cdragon_rune_full": td(hours=1),
            "cdragon_profile_icon_full": td(hours=1),
            "cdragon_spells_full": td(hours=1),

            "meraki_champion_by_key": td(hours=3),
            "meraki_item_by_id": td(hours=3),
        },
        "tft": {
            "account_v1_by_puuid": td(hours=1),
            "account_v1_active_shard": 0,
            "league_v1_summoner_entries": 0,
            "league_v1_challenger_league": td(hours=1),
            "league_v1_grandmaster_league": td(hours=1),
            "league_v1_master_league": td(hours=1),
            "league_v1_entries_by_division": 0,
            "league_v1_league_by_league_id": 0,
            "match_v1_match": td(days=7),
            "match_v1_matchlist": td(minutes=5),
            "summoner_v1_by_name": td(hours=1),
            "summoner_v1_by_id": td(hours=1),
            "summoner_v1_by_account_id": td(hours=1),
            "summoner_v1_by_puuid": td(hours=1),

            "cdragon_tft_full": td(hours=1),
            "cdragon_profile_icon_full": td(hours=1),
        },
        "val": {
            "account_v1_by_puuid": td(hours=1),
            "account_v1_by_riot_id": td(hours=1),
            "account_v1_active_shard": 0,
            "match_v1_match": td(days=7),
            "match_v1_matchlist": 0,
            "content_v1_contents": td(hours=3),
        }
    }

    def __init__(self, game, custom_expirations: Dict):
        self.expirations = copy.deepcopy(self._expirations[game]) 
        if custom_expirations is not None:
            if "*" in custom_expirations:
                for key in self.expirations:
                    if key not in custom_expirations:
                        custom_expirations[key] = custom_expirations["*"]
                custom_expirations.pop("*")
            for key in custom_expirations:
                if key not in self.expirations:
                    raise RuntimeError(f"'{key}' is not a valid expiration token")
            self.expirations.update(custom_expirations)
        self.expirations = self._create_expiration(self.expirations)

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
        try:
            return self.expirations[key]
        except KeyError:
            LOGGER.warning("[Trace: Pyot Pipeline] WARNING: A non defined expiration token was passed, returned 0 by default")
            return 0


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
            if code not in self.default_handler:
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
        hand = copy.deepcopy(self.default_handler)
        hand.update(handler)
        return hand