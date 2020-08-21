from .__core__ import PyotStoreObject, PyotRequestToken, PyotErrorHandler
from ..core import exceptions as exc
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from typing import Mapping, Tuple, Dict, List, Any
from ..core.pipeline import PyotPipelineToken
from json.decoder import JSONDecodeError
from ..core.lock import PyotLock
import asyncio
import aiohttp

from logging import getLogger
LOGGER = getLogger(__name__)


@dataclass
class RiotAPILimitToken:
    _token: List[int] = field(default_factory=list)

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
            await asyncio.sleep(self.max)
            return True
        else:
            return False


class RiotAPIRateLimiter:
    default_rates = {
        "lol": {
            "champion-v3-rotation":                  [[None, 0, 30, 10], [None, 0, 500, 600]],
            "champion-mastery-v4-all-mastery":       [[None, 0, 2000, 60],[None, 0, 2000, 60]],
            "champion-mastery-v4-by-champion-id":    [[None, 0, 2000, 60],[None, 0, 2000, 60]],
            "clash-v1-players":                      [[None, 0, 200, 60],[None, 0, 200, 60]],
            "clash-v1-teams":                        [[None, 0, 200, 60],[None, 0, 200, 60]],
            "clash-v1-tournaments-by-team-id":       [[None, 0, 200, 60],[None, 0, 200, 60]],
            "clash-v1-toutnaments-by-tournament-id": [[None, 0, 10, 60],[None, 0, 10, 60]],
            "clash-v1-tournaments-all":              [[None, 0, 10, 60],[None, 0, 10, 60]],
            "league-v4-summoner-entries":            [[None, 0, 270, 60],[None, 0, 270, 60]],
            "league-v4-challenger-league":           [[None, 0, 30, 10],[None, 0, 500, 600]],
            "league-v4-grandmaster-league":          [[None, 0, 30, 10],[None, 0, 500, 600]],
            "league-v4-master-league":               [[None, 0, 30, 10],[None, 0, 500, 600]],
            "league-v4-entries-by-division":         [[None, 0, 10, 2],[None, 0, 10, 2]],
            "league-v4-league-by-league-id":         [[None, 0, 500, 10],[None, 0, 500, 10]],
            "status-v3-shard-data":                  [[None, 1, 30, 10],[None, 1, 500, 600]],
            "match-v4-match":                        [[None, 0, 500, 10],[None, 0, 500, 10]],
            "match-v4-timeline":                     [[None, 0, 500, 10],[None, 0, 500, 10]],
            "match-v4-matchlist":                    [[None, 0, 1000, 10],[None, 0, 1000, 10]],
            "spectator-v4-current-game":             [[None, 0, 20000, 10],[None, 0, 1200000, 600]],
            "spectator-v4-featured-games":           [[None, 0, 20000, 10],[None, 0, 1200000, 600]],
            "summoner-v4-by-name":                   [[None, 0, 2000, 60],[None, 0, 2000, 60]],
            "summoner-v4-by-id":                     [[None, 0, 2000, 60],[None, 0, 2000, 60]],
            "summoner-v4-by-account-id":             [[None, 0, 2000, 60],[None, 0, 2000, 60]],
            "summoner-v4-by-puuid":                  [[None, 0, 2000, 60],[None, 0, 2000, 60]],
            "third-party-code-v4-code":              [[None, 0, 500, 10],[None, 0, 500, 10]],
        },
        "val": {
            "account-v1-by-puuid":     [[None, 0, 1000, 60],[None, 0, 1000, 60]],
            "account-v1-by-riot-id":   [[None, 0, 1000, 60],[None, 0, 1000, 60]],
            "account-v1-active-shard": [[None, 0, 1000, 60],[None, 0, 1000, 60]],
            "match-v1-match":          [[None, 0, 500, 10],[None, 0, 500, 10]],  # I DUNNO, RIOT IS DEPRESSING ME
            "match-v1-matchlist":      [[None, 0, 500, 10],[None, 0, 500, 10]],
            "content-v1-contents":     [[None, 0, 60, 60],[None, 0, 60, 60]],
        }
    }

    def __init__(self, game, share):
        yesterday = datetime.now() - timedelta(days=1)
        self._lock = PyotLock()
        self._share = share
        self._methods_rates = self.default_rates[game]
        self._methods_times = { key: [yesterday, yesterday] for key in self.default_rates[game] }
        self._methods_backoffs = { key: yesterday for key in self.default_rates[game] }
        self._application_rates = [[None, 1, 20, 1],[None, 1, 100, 120]]
        self._application_times = [yesterday, yesterday]
        self._application_backoffs = yesterday
        
        # Rates are recorded as [minumum_call_backed, current_call_passed, max_call_allowed, time_span]

    async def get_limit_token(self, method: str) -> RiotAPILimitToken:
        async with self._lock:
            token = RiotAPILimitToken()
            app_rate1 = self._application_rates[0]
            app_rate2 = self._application_rates[1]
            app_time1 = self._application_times[0]
            app_time2 = self._application_times[1]
            now = datetime.now()
            try:
                method_rate1 = self._methods_rates[method][0]
                method_rate2 = self._methods_rates[method][1]
                method_time1 = self._methods_times[method][0]
                method_time2 = self._methods_times[method][1]
            except KeyError:
                self._methods_rates[method] = [[None,0,20,1],[None,0,20,60]]
                self._methods_times[method] = [now - timedelta(days=1), now - timedelta(days=1)]
                self._methods_backoffs[method] = now-timedelta(days=1)
                method_rate1 = self._methods_rates[method][0]
                method_rate2 = self._methods_rates[method][1]
                method_time1 = self._methods_times[method][0]
                method_time2 = self._methods_times[method][1]
            if app_time1 < now:
                app_time1 = self._application_times[0] = now + timedelta(seconds=app_rate1[3]+1)
                app_rate1[0] = self._application_rates[0][0] = None
                app_rate1[1] = self._application_rates[0][1] = 0
            if app_time2 < now:
                app_time2 = self._application_times[1] = now + timedelta(seconds=app_rate2[3]+1)
                app_rate2[0] = self._application_rates[1][0] = None
                app_rate2[1] = self._application_rates[1][1] = 0
            if method_time1 < now:
                method_time1 = self._methods_times[method][0] = now + timedelta(seconds=method_rate1[3]+1)
                method_rate1[0] = self._methods_rates[method][0][0] = None
                method_rate1[1] = self._methods_rates[method][0][1] = 0
            if method_time2 < now:
                method_time2 = self._methods_times[method][1] = now + timedelta(seconds=method_rate2[3]+1)
                method_rate2[0] = self._methods_rates[method][1][0] = None
                method_rate2[1] = self._methods_rates[method][1][1] = 0

            i_rates = [app_rate1, app_rate2, method_rate1, method_rate2]
            i_times = [app_time1, app_time2, method_time1, method_time2]
            for i in range(4):
                if i_rates[i][0] and i_rates[i][0] + i_rates[i][1] - 1 > int(i_rates[i][2]*self._share):
                    token.append((i_times[i]-now).total_seconds())
                else:
                    token.append(0)

            if self._application_backoffs > now:
                token.append((self._application_backoffs-now).total_seconds())

            if self._methods_backoffs[method] > now:
                token.append((self._methods_backoffs[method]-now).total_seconds())


            if token.max == 0:
                for i in range(4):
                    i_rates[i][1] += 1

            return token

    async def stream(self, response: Any, method: str):
        headers = response.headers if hasattr(response, "headers") else None
        if headers:
            try:
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
                        if self._application_rates[0][i+2] != app_limit[0][i]:
                            self._application_rates[0][i+2] = app_limit[0][i]
                        if self._application_rates[1][i+2] != app_limit[1][i]:
                            self._application_rates[1][i+2] = app_limit[1][i]
                        if self._methods_rates[method][0][i+2] != method_limit[0][i]:
                            self._methods_rates[method][0][i+2] = method_limit[0][i]
                        if self._methods_rates[method][1][i+2] != method_limit[1][i]:
                            self._methods_rates[method][1][i+2] = method_limit[1][i]
                    for i in range(2):
                        if self._application_rates[i][0] is None or app_count[i][0] < self._application_rates[i][0]:
                            self._application_rates[i][0] = app_count[i][0]
                        if self._methods_rates[method][i][0] is None or method_count[i][0] < self._methods_rates[method][i][0]:
                            self._methods_rates[method][i][0] = method_count[i][0]
            except Exception:
                LOGGER.warning("[Trace: RiotAPI] Something unexpected happened while streaming to rate limiter")

    async def inmediate_backoff(self, seconds: int, type_: str, method: str = None):
        async with self._lock:
            time = datetime.now() + timedelta(seconds=seconds)
            if type_ == "application":
                self._application_backoffs = time
            else:
                self._methods_backoffs[method] = time


class RiotAPIEndpoint:
    _endpoints = {
        "lol": {
            "champion-v3-rotation": "/lol/platform/v3/champion-rotations",
            "champion-mastery-v4-by-champion-id": "/lol/champion-mastery/v4/champion-masteries/by-summoner/{summoner_id}/by-champion/{champion_id}",
            "champion-mastery-v4-all-mastery": "/lol/champion-mastery/v4/champion-masteries/by-summoner/{summoner_id}",
            "clash-v1-players": "/lol/clash/v1/players/by-summoner/{summoner_id}",
            "clash-v1-teams": "/lol/clash/v1/teams/{id}",
            "clash-v1-tournaments-by-team-id": "/lol/clash/v1/tournaments/by-team/{team_id}",
            "clash-v1-toutnaments-by-tournament-id": "/lol/clash/v1/tournaments/{id}",
            "clash-v1-tournaments-all": "/lol/clash/v1/tournaments",
            "league-v4-summoner-entries": "/lol/league/v4/entries/by-summoner/{summoner_id}",
            "league-v4-challenger-league": "/lol/league/v4/challengerleagues/by-queue/{queue}",
            "league-v4-grandmaster-league": "/lol/league/v4/grandmasterleagues/by-queue/{queue}",
            "league-v4-master-league": "/lol/league/v4/masterleagues/by-queue/{queue}",
            "league-v4-entries-by-division": "/lol/league/v4/entries/{queue}/{tier}/{division}",
            "league-v4-league-by-league-id": "/lol/league/v4/leagues/{id}",
            "status-v3-shard-data": "/lol/status/v3/shard-data",
            "match-v4-match": "/lol/match/v4/matches/{id}",
            "match-v4-timeline": "/lol/match/v4/timelines/by-match/{id}",
            "match-v4-matchlist": "/lol/match/v4/matchlists/by-account/{account_id}",
            "spectator-v4-current-game": "/lol/spectator/v4/active-games/by-summoner/{summoner_id}",
            "spectator-v4-featured-games": "/lol/spectator/v4/featured-games",
            "summoner-v4-by-name": "/lol/summoner/v4/summoners/by-name/{name}",
            "summoner-v4-by-id": "/lol/summoner/v4/summoners/{id}",
            "summoner-v4-by-account-id": "/lol/summoner/v4/summoners/by-account/{account_id}",
            "summoner-v4-by-puuid": "/lol/summoner/v4/summoners/by-puuid/{puuid}",
            "third-party-code-v4-code": "/lol/platform/v4/third-party-code/by-summoner/{summoner_id}",
        },
        "val": {
            "account-v1-by-puuid": "/riot/account/v1/accounts/by-puuid/{puuid}",
            "account-v1-by-riot-id": "/riot/account/v1/accounts/by-riot-id/{name}/{tag}",
            "account-v1-active-shard": "/riot/account/v1/active-shards/by-game/{game}/by-puuid/{puuid}",
            "match-v1-match": "/val/match/v1/matches/{id}",
            "match-v1-matchlist": "/val/match/v1/matchlists/by-puuid/{puuid}",
            "content-v1-contents": "/val/content/v1/contents",
        }
    }
    
    _base_url = "https://{server}.api.riotgames.com"

    def __init__(self, game):
        self.endpoints = self._endpoints[game]

    async def resolve(self, token: PyotPipelineToken) -> str:
        try:
            base = self._base_url.format(**{"server": token.server.lower()})
            url = self.endpoints[token.method].format(**token.params)
            query = ""
            for a, b in token.queries.items():
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
        self._endpoints = RiotAPIEndpoint(game)
        self._limiting_share = validator.create_share(limiting_share)
        self._rate_limiter = RiotAPIRateLimiter(game, self._limiting_share)
        self._handler_map = validator.create_handler(error_handling)
        self._logs_enabled = logs_enabled
        self._api_key = key

    async def initialize(self):
        headers = { "X-Riot-Token": self._api_key }
        url = "https://na1.api.riotgames.com/lol/status/v3/shard-data"
        async with aiohttp.ClientSession() as session: # type: aiohttp.ClientSession
            try:
                LOGGER.warning("[Trace: RiotAPI] Store initializing ...")
                response = await session.request("GET", url, headers=headers)
            except RuntimeError:
                raise RuntimeError(f"Pyot coroutines need to be executed inside PyotPipeline loop")
            if response and response.status == 200:
                await self._rate_limiter.stream(response, "status-v3-shard-data")
            else:
                raise RuntimeError("[Trace: RiotAPI]: Store failed initialize, "+
                    f"the preflight call responded with status code {response.status}")

    async def get(self, token: PyotPipelineToken) -> Dict:
        method = token.method
        url = await self._endpoints.resolve(token)
        headers = { "X-Riot-Token": self._api_key }
        request_token = PyotRequestToken()
        async with aiohttp.ClientSession() as session: # type: aiohttp.ClientSession
            while await request_token.run_or_raise():
                try:
                    limit_token = await self._rate_limiter.get_limit_token(method)
                    if await limit_token.run_or_wait():
                        continue
                    if self._logs_enabled:
                        LOGGER.warning(f"[Trace: RiotAPI] GET: {self._log_template(token)}")
                    response = await session.request("GET", url, headers=headers)
                except RuntimeError:
                    raise RuntimeError(f"Pyot coroutines need to be executed inside PyotPipeline loop")
                except Exception:
                    response = None
                
                await self._rate_limiter.stream(response, method)
                if response and response.status == 200:
                    try:
                        return await response.json(encoding="utf-8")
                    except JSONDecodeError:
                        return await response.text()

                code = response.status if response is not None else 408
                how = self._handler_map[code] if self._handler_map[code] else self._handler_map[888]
                await self._check_backoff(response, method, code)
                await request_token.stream(code, how)
    
    async def _check_backoff(self, response: Any, method: str, code: int):
        if code == 429 and hasattr(response, "headers") and "X-Rate-Limit-Type" in response.headers and response.headers["X-Rate-Limit-Type"] != "service":
            LOGGER.warning(f"[Trace: RiotAPI] FATAL: The server responded with a non service 429, interrupts your task if this persists")
            seconds = response.headers["Retry-After"] if "Retry-After" in response.headers else 5
            type_ = response.headers["X-Rate-Limit-Type"]
            self._rate_limiter.inmediate_backoff(seconds, type_, method)

