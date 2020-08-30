from .__core__ import PyotStoreObject, PyotRequestToken, PyotErrorHandler
from ..core import exceptions as exc
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from typing import Mapping, Tuple, Dict, List, Any
from ..core.pipeline import PyotPipelineToken
from json.decoder import JSONDecodeError
from collections import defaultdict
from dateutil.parser import parse
from ..core.lock import PyotLock
import asyncio
import aiohttp
import pytz

from logging import getLogger
LOGGER = getLogger(__name__)


@dataclass
class RiotAPILimitToken:
    _token: List[int] = field(default_factory=list)
    flag: bool = False

    def append(self, val: int):
        self._token.append(val)

    @property
    def max(self) -> int:
        val = max(self._token)
        if val >= 0:
            return val
        else:
            return 0

    async def run_or_wait(self):
        if self.max > 0:
            # if self.max > 1: print(self.max)
            await asyncio.sleep(self.max)
            return True
        else:
            return False


class RiotAPIRateLimiter:

    def __init__(self, game, share):
        yesterday = datetime.now(pytz.utc) - timedelta(days=1)
        self._game = game
        self._lock = PyotLock()
        self._share = share
        self._methods_rates = defaultdict(lambda: [[None, 1, 10, 60], [None, 1, 10, 60]])
        self._methods_times = defaultdict(lambda: [yesterday, yesterday])
        self._methods_backoffs = defaultdict(lambda: yesterday)
        self._application_rates = defaultdict(lambda: [[None, 1, 20, 1],[None, 1, 100, 120]])
        self._application_times = defaultdict(lambda: [yesterday, yesterday])
        self._application_backoffs = defaultdict(lambda: yesterday)
        self._methods_bucket = defaultdict(lambda: 0)
        self._application_bucket = defaultdict(lambda: 0)
        
        # Rates are recorded as [minumum_call_backed, current_call_passed, max_call_allowed, time_span]

    async def get_limit_token(self, server: str, method: str) -> RiotAPILimitToken:
        async with self._lock:
            token = RiotAPILimitToken()
            app_rate1 = self._application_rates[server][0]
            app_rate2 = self._application_rates[server][1]
            app_time1 = self._application_times[server][0]
            app_time2 = self._application_times[server][1]
            now = datetime.now(pytz.utc)
            method_rate1 = self._methods_rates[method][0]
            method_rate2 = self._methods_rates[method][1]
            method_time1 = self._methods_times[method][0]
            method_time2 = self._methods_times[method][1]
            if app_time1 < now:
                app_time1 = self._application_times[server][0] = now + timedelta(seconds=app_rate1[3])
                app_rate1[0] = self._application_rates[server][0][0] = None
                app_rate1[1] = self._application_rates[server][0][1] = 0
            if app_time2 < now:
                app_time2 = self._application_times[server][1] = now + timedelta(seconds=app_rate2[3])
                app_rate2[0] = self._application_rates[server][1][0] = None
                app_rate2[1] = self._application_rates[server][1][1] = 0
            if method_time1 < now:
                method_time1 = self._methods_times[method][0] = now + timedelta(seconds=method_rate1[3])
                method_rate1[0] = self._methods_rates[method][0][0] = None
                method_rate1[1] = self._methods_rates[method][0][1] = 0
            if method_time2 < now:
                method_time2 = self._methods_times[method][1] = now + timedelta(seconds=method_rate2[3])
                method_rate2[0] = self._methods_rates[method][1][0] = None
                method_rate2[1] = self._methods_rates[method][1][1] = 0

            i_rates = [app_rate1, app_rate2, method_rate1, method_rate2]
            i_times = [app_time1, app_time2, method_time1, method_time2]
            
            for i in range(4):
                if i_rates[i][0] and  i_rates[i][0] + i_rates[i][1] - 1 >= int(i_rates[i][2]*self._share):
                    token.append((i_times[i]-now).total_seconds())
                else:
                    token.append(0)

            if self._application_backoffs[server] > now:
                token.append((self._application_backoffs[server]-now).total_seconds())

            if self._methods_backoffs[method] > now:
                token.append((self._methods_backoffs[method]-now).total_seconds())


            if token.max == 0:
                if self._application_rates[server][0][0] is None and self._application_bucket[server] == 0:
                    self._application_bucket[server] += 1
                    token.flag = True
                    token.append(0)
                elif self._application_rates[server][0][0] is None and self._application_bucket[server] > 0:
                    token.append(0.5)

                if self._methods_rates[method][0][0] is None and self._methods_bucket[method] == 0 and token.max == 0:
                    self._methods_bucket[method] += 1
                    token.flag = True
                    token.append(0)
                elif self._methods_rates[method][0][0] is None and self._methods_bucket[method] > 0:
                    token.append(0.5)

            if token.max == 0:
                for i in range(4):
                    i_rates[i][1] += 1

            return token

    async def stream(self, response: Any, server: str, method: str, token: RiotAPILimitToken):
        headers = response.headers if hasattr(response, "headers") else None
        if headers:
            try:
                date = parse(headers["Date"].split(', ')[1])
                app_limit = [[int(val) for val in token.split(':')] for token in headers["X-App-Rate-Limit"].split(',')]
                app_count = [[int(val) for val in token.split(':')] for token in headers["X-App-Rate-Limit-Count"].split(',')]
                method_limit = [[int(val) for val in token.split(':')] for token in headers["X-Method-Rate-Limit"].split(',')]
                method_count = [[int(val) for val in token.split(':')] for token in headers["X-Method-Rate-Limit-Count"].split(',')]
                if len(method_limit) == 1:
                    method_limit.append(method_limit[0])
                if len(method_count) == 1:
                    method_count.append(method_count[0])
                async with self._lock:
                    for i in range(2):
                        if self._application_rates[server][0][i+2] != app_limit[0][i]:
                            self._application_rates[server][0][i+2] = app_limit[0][i]
                        if self._application_rates[server][1][i+2] != app_limit[1][i]:
                            self._application_rates[server][1][i+2] = app_limit[1][i]
                        if self._methods_rates[method][0][i+2] != method_limit[0][i]:
                            self._methods_rates[method][0][i+2] = method_limit[0][i]
                        if self._methods_rates[method][1][i+2] != method_limit[1][i]:
                            self._methods_rates[method][1][i+2] = method_limit[1][i]
                    for i in range(2):
                        if token.flag and self._application_bucket[server] > 0:
                            self._application_bucket[server] -= 1
                        if token.flag and self._methods_bucket[method] > 0:
                            self._methods_bucket[method] -= 1
                    for i in range(2):
                        if not self._application_rates[server][i][0] or app_count[i][0] < self._application_rates[server][i][0]:
                            self._application_rates[server][i][0] = app_count[i][0]
                        if not self._methods_rates[method][i][0] or method_count[i][0] < self._methods_rates[method][i][0]:
                            self._methods_rates[method][i][0] = method_count[i][0]
                    for i in range(2):
                        app_top = date + timedelta(seconds=self._application_rates[server][i][3])
                        method_top = date + timedelta(seconds=self._methods_rates[method][i][3])
                        if app_top < self._application_times[server][i] or token.flag:
                            self._application_times[server][i] = app_top
                        if method_top < self._methods_times[method][i] or token.flag:
                            self._methods_times[method][i] = method_top
            except Exception:
                LOGGER.warning(f"[Trace: {self._game.upper()} > RiotAPI] Something unexpected happened while streaming to rate limiter")

    async def inmediate_backoff(self, seconds: int, type_: str, server: str, method: str = None):
        async with self._lock:
            time = datetime.now(pytz.utc) + timedelta(seconds=seconds)
            if type_ == "application":
                self._application_backoffs[server] = time
            else:
                self._methods_backoffs[method] = time


class RiotAPIEndpoint:
    _endpoints = {
        "lol": {
            "account_v1_by_puuid": "/riot/account/v1/accounts/by-puuid/{puuid}",
            "account_v1_active_shard": "/riot/account/v1/active-shards/by-game/{game}/by-puuid/{puuid}",
            "champion_v3_rotation": "/lol/platform/v3/champion-rotations",
            "champion_mastery_v4_by_champion_id": "/lol/champion-mastery/v4/champion-masteries/by-summoner/{summoner_id}/by-champion/{champion_id}",
            "champion_mastery_v4_all_mastery": "/lol/champion-mastery/v4/champion-masteries/by-summoner/{summoner_id}",
            "clash_v1_players": "/lol/clash/v1/players/by-summoner/{summoner_id}",
            "clash_v1_teams": "/lol/clash/v1/teams/{id}",
            "clash_v1_tournaments_by_team_id": "/lol/clash/v1/tournaments/by-team/{team_id}",
            "clash_v1_toutnaments_by_tournament_id": "/lol/clash/v1/tournaments/{id}",
            "clash_v1_tournaments_all": "/lol/clash/v1/tournaments",
            "league_v4_summoner_entries": "/lol/league/v4/entries/by-summoner/{summoner_id}",
            "league_v4_challenger_league": "/lol/league/v4/challengerleagues/by-queue/{queue}",
            "league_v4_grandmaster_league": "/lol/league/v4/grandmasterleagues/by-queue/{queue}",
            "league_v4_master_league": "/lol/league/v4/masterleagues/by-queue/{queue}",
            "league_v4_entries_by_division": "/lol/league/v4/entries/{queue}/{tier}/{division}",
            "league_v4_league_by_league_id": "/lol/league/v4/leagues/{id}",
            "status_v3_shard_data": "/lol/status/v3/shard-data",
            "match_v4_match": "/lol/match/v4/matches/{id}",
            "match_v4_timeline": "/lol/match/v4/timelines/by-match/{id}",
            "match_v4_matchlist": "/lol/match/v4/matchlists/by-account/{account_id}",
            "spectator_v4_current_game": "/lol/spectator/v4/active-games/by-summoner/{summoner_id}",
            "spectator_v4_featured_games": "/lol/spectator/v4/featured-games",
            "summoner_v4_by_name": "/lol/summoner/v4/summoners/by-name/{name}",
            "summoner_v4_by_id": "/lol/summoner/v4/summoners/{id}",
            "summoner_v4_by_account_id": "/lol/summoner/v4/summoners/by-account/{account_id}",
            "summoner_v4_by_puuid": "/lol/summoner/v4/summoners/by-puuid/{puuid}",
            "third_party_code_v4_code": "/lol/platform/v4/third-party-code/by-summoner/{summoner_id}",
        },
        "tft": {
            "account_v1_by_puuid": "/riot/account/v1/accounts/by-puuid/{puuid}",
            "account_v1_active_shard": "/riot/account/v1/active-shards/by-game/{game}/by-puuid/{puuid}",
            "league_v1_summoner_entries": "/tft/league/v1/entries/by-summoner/{summoner_id}",
            "league_v1_challenger_league": "/tft/league/v1/challenger",
            "league_v1_grandmaster_league": "/tft/league/v1/grandmaster",
            "league_v1_master_league": "/tft/league/v1/master",
            "league_v1_entries_by_division": "/tft/league/v1/entries/{tier}/{division}",
            "league_v1_league_by_league_id": "/tft/league/v1/leagues/{id}",
            "match_v1_matchlist": "/tft/match/v1/matches/by-puuid/{puuid}/ids",
            "match_v1_match": "/tft/match/v1/matches/{id}",
            "summoner_v1_by_name": "/tft/summoner/v1/summoners/by-name/{name}",
            "summoner_v1_by_id": "/tft/summoner/v1/summoners/{id}",
            "summoner_v1_by_account_id": "/tft/summoner/v1/summoners/by-account/{account_id}",
            "summoner_v1_by_puuid": "/tft/summoner/v1/summoners/by-puuid/{puuid}",
        },
        "val": {
            "account_v1_by_puuid": "/riot/account/v1/accounts/by-puuid/{puuid}",
            "account_v1_by_riot_id": "/riot/account/v1/accounts/by-riot-id/{name}/{tag}",
            "account_v1_active_shard": "/riot/account/v1/active-shards/by-game/{game}/by-puuid/{puuid}",
            "match_v1_match": "/val/match/v1/matches/{id}",
            "match_v1_matchlist": "/val/match/v1/matchlists/by-puuid/{puuid}",
            "content_v1_contents": "/val/content/v1/contents",
        }
    }

    _initializers = {
        "lol": "https://na1.api.riotgames.com/lol/status/v3/shard-data",
        "tft": "https://na1.api.riotgames.com/tft/league/v1/challenger",
        "val": "https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/stelar7/stl7",
    }
    
    _base_url = "https://{server}.api.riotgames.com"

    def __init__(self, game):
        self.endpoints = self._endpoints[game]

    async def resolve(self, token: PyotPipelineToken) -> str:
        try:
            base = self._base_url.format(**{"server": token.server})
            url = self.endpoints[token.method].format(**token.params)
            query = ""
            for a, b in token.queries.items():
                if isinstance(b, list):
                    for val in b:
                        query = query + "&" + str(a) + "=" + str(val)
                else:
                    query = query + "&" + str(a) + "=" + str(b)
            if len(query) > 1:
                query= "?" + query[1:]
            return base + url + query
        except KeyError:
            raise exc.NotFound


class RiotAPIValidate(PyotErrorHandler):
    
    def create_share(self, limiting_share):
        if limiting_share > 1 or limiting_share < 0:
            raise AttributeError("'API_LIMITING_SHARE' should be a float between 0 and 1")
        return limiting_share


class RiotAPI(PyotStoreObject):
    unique = True
    
    def __init__(self, game: str, key: str, limiting_share: float = 1, error_handling: Mapping[int, Any] = None, logs_enabled: bool = True):
        validator = RiotAPIValidate()
        self._game = game
        self._endpoints = RiotAPIEndpoint(game)
        self._limiting_share = validator.create_share(limiting_share)
        self._rate_limiter = RiotAPIRateLimiter(game, self._limiting_share)
        self._handler_map = validator.create_handler(error_handling)
        self._logs_enabled = logs_enabled
        self._api_key = key

    async def initialize(self):
        headers = { "X-Riot-Token": self._api_key }
        url = self._endpoints._initializers[self._game]
        async with aiohttp.ClientSession() as session: # type: aiohttp.ClientSession
            try:
                LOGGER.warning(f"[Trace: {self._game.upper()} > RiotAPI] Store initializing ...")
                response = await session.request("GET", url, headers=headers)
            except RuntimeError:
                raise RuntimeError(f"Pyot coroutines need to be executed inside PyotPipeline loop")
            if response and response.status == 200:
                token = RiotAPILimitToken()
                await self._rate_limiter.stream(response, "na1", "na1status-v3-shard-data", token)
            else:
                raise RuntimeError(f"[Trace: {self._game.upper()} > RiotAPI]: Store failed to initialize, "+
                    f"the server responded with status code {response.status} to the preflight call")

    async def get(self, token: PyotPipelineToken, session: aiohttp.ClientSession) -> Dict:
        method = token.method
        server = token.server
        url = await self._endpoints.resolve(token)
        headers = { "X-Riot-Token": self._api_key }
        request_token = PyotRequestToken()
        while await request_token.run_or_raise():
            try:
                limit_token = await self._rate_limiter.get_limit_token(server, server+method)
                if await limit_token.run_or_wait():
                    continue
                if self._logs_enabled:
                    LOGGER.warning(f"[Trace: {self._game.upper()} > RiotAPI] GET: {self._log_template(token)}")
                response = await session.request("GET", url, headers=headers)
            except RuntimeError:
                raise RuntimeError(f"Pyot coroutines need to be executed inside PyotPipeline loop")
            except Exception as e:
                LOGGER.warning(f"[Trace: {self._game.upper()} > RiotAPI] WARNING: '{e.__class__.__name__}: {e}' was raised during the request and ignored")
                response = None
            
            await self._rate_limiter.stream(response, server, server+method, limit_token)
            if response and response.status == 200:
                try:
                    return await response.json(encoding="utf-8")
                except JSONDecodeError:
                    return await response.text()

            code = response.status if response is not None else 408
            how = self._handler_map[code] if self._handler_map[code] else self._handler_map[888]
            await self._check_backoff(response, server, method, code)
            await request_token.stream(code, how)
    
    async def _check_backoff(self, response: Any, server: str, method: str, code: int):
        if code == 429 and hasattr(response, "headers") and "X-Rate-Limit-Type" in response.headers and response.headers["X-Rate-Limit-Type"] != "service":
            LOGGER.warning(f"[Trace: {self._game.upper()} > RiotAPI] FATAL: The server responded with a non service 429, interrupts your task if this persists")
            seconds = response.headers["Retry-After"] if "Retry-After" in response.headers else 5
            type_ = response.headers["X-Rate-Limit-Type"]
            await self._rate_limiter.inmediate_backoff(int(seconds), type_, server, server+method)


