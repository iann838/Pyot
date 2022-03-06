from time import time
from typing import Dict, List, Union

from aiohttp import ClientResponse
import aioredis

from pyot.utils.locks import SealLock
from pyot.utils.eventloop import EventLoopFactory

from .base import BaseLimiter, LimiterToken


class RedisLimiter(BaseLimiter):

    def __init__(self, game: str, api_key: str, host='127.0.0.1', port=6379, db=0, limiting_share=1, **kwargs):
        self.game = game
        self.api_key = api_key
        self.api_hash = api_key[-5:]
        self.limiting_share = limiting_share
        self.lock = SealLock()
        self.redis = EventLoopFactory(
            factory=lambda: aioredis.create_redis_pool(f"redis://{host}:{port}/{db}", **kwargs),
            callback=lambda pool: pool.close(),
        )
        self.shas: Dict[str, str] = None
        self.latency = 0.002

    async def register_scripts(self):
        get_token_lua = '''
        local sleep = 0
        local allowed = {}
        local pinging_list = {}
        local app_prefix = KEYS[1]
        local method_prefix = KEYS[2]
        local now = tonumber(ARGV[1])
        local prefix_groups = {{app_prefix, 0, "app"}, {app_prefix, 1, "app"}, {method_prefix, 0, "method"}, {method_prefix, 1, "method"}}
        for j=1, 4 do
            local outerbreak = 0
            repeat
                local prefix, i, type = unpack(prefix_groups[j])
                local prefix_i = prefix..":"..i
                local exists = redis.call("GET", prefix_i..":exists")
                if exists == "0" then
                    break
                end
                local freeze = tonumber(redis.call("GET", prefix_i..":freeze"))
                if (freeze or 0) > now then
                    sleep = math.max(sleep, freeze - now)
                    break
                end
                local pinging = redis.call("GET", prefix_i..":pinging")
                local pingexp = tonumber(redis.call("GET", prefix_i..":pingexp"))
                if now > (pingexp or 0) then
                    pinging = 0
                end
                if pinging == "1" then
                    sleep = math.max(sleep, 0.1)
                    outerbreak = 1
                    break
                end
                local maxcall = tonumber(redis.call("GET", prefix_i..":maxcall"))
                local rollover = tonumber(redis.call("GET", prefix_i..":rollover"))
                local timespan = tonumber(redis.call("GET", prefix_i..":timespan"))
                local called = tonumber(redis.call("GET", prefix_i..":called"))
                local begintime = tonumber(redis.call("GET", prefix_i..":begintime"))
                local pingtime = tonumber(redis.call("GET", prefix_i..":pingtime"))
                local blackout
                local nextstart
                local qualified
                if maxcall ~= nil then
                    blackout = begintime + timespan
                    nextstart = blackout + pingtime
                    qualified = nextstart - now
                end
                if maxcall == nil or now > nextstart then
                    redis.call("SET", prefix_i..":pinging", 1)
                    redis.call("SET", prefix_i..":pingexp", tostring(now + 10))
                    redis.call("SET", prefix_i..":pingbegintime", tostring(now))
                    table.insert(pinging_list, {prefix_i, type, i})
                    break
                end
                if (rollover or 0) + called >= maxcall then
                    sleep = math.max(sleep, qualified)
                    break
                end
                if now >= blackout then
                    sleep = math.max(sleep, qualified)
                    break
                end
                table.insert(allowed, prefix_i)
                break
            until 1
            if outerbreak == 1 then
                break
            end
        end
        if sleep == 0 then
            for i=1, #allowed do
                local allow = allowed[i]
                redis.call("INCR", allow..":called")
                if #pinging_list == 0 then
                    redis.call("INCR", allow..":flying")
                end
            end
        else
            for i=1, #pinging_list do
                local prefix_i, type = unpack(pinging_list[i])
                redis.call("SET", prefix_i..":pinging", 0)
            end
            pinging_list = {}
        end
        local pinging_string = ""
        for i=1, #pinging_list do
            for j=1, #pinging_list[i] do
                pinging_string = pinging_string..tostring(pinging_list[i][j])..","
            end
            pinging_string = pinging_string..";"
        end
        local allowed_string = ""
        for i=1, #allowed do
            allowed_string = allowed_string..tostring(allowed[i])..";"
        end
        return {tostring(sleep), allowed_string, pinging_string}
        '''
        sync_rates_ping_lua = '''
        local now = tonumber(ARGV[1])
        for i=1, #KEYS do
            local keyi = i * 4 - 3
            local prefix_i = KEYS[i]
            local exists = ARGV[keyi + 1]
            redis.call("SET", prefix_i..":exists", exists)
            if exists == "1" then
                redis.call("SET", prefix_i..":maxcall", ARGV[keyi + 2])
                redis.call("SET", prefix_i..":timespan", ARGV[keyi + 3])
                redis.call("SET", prefix_i..":called", ARGV[keyi + 4])
                local flying = redis.call("GET", prefix_i..":flying")
                redis.call("SET", prefix_i..":rollover", (flying or 0))
                redis.call("SET", prefix_i..":flying", 0)
                local begintime = tonumber(redis.call("GET", prefix_i..":pingbegintime"))
                redis.call("SET", prefix_i..":begintime", tostring(begintime))
                redis.call("SET", prefix_i..":pingtime", tostring(now - begintime))
                redis.call("SET", prefix_i..":pinging", 0)
            end
        end
        return 1
        '''
        sync_rates_land_lua = '''
        local epoch = tonumber(ARGV[1])
        for i=1, #KEYS do
            local prefix_i = KEYS[i]
            local begintime = tonumber(redis.call("GET", prefix_i..":begintime"))
            if epoch >= begintime then
                redis.call("DECR", prefix_i..":flying")
            end
        end
        return 1
        '''
        ping_fail_lua = '''
        for i=1, #KEYS do
            redis.call("SET", KEYS[i]..":pinging", 0)
        end
        '''
        freeze_rates_lua = '''
        local now = tonumber(ARGV[1])
        local time = ARGV[2]
        for i=1, #KEYS do
            redis.call("SET", KEYS[i]..":freeze", tostring(now + time))
        end
        '''
        redis = await self.redis.get()
        return {
            "get_token": await redis.script_load(get_token_lua),
            "sync_rates.ping": await redis.script_load(sync_rates_ping_lua),
            "sync_rates.land": await redis.script_load(sync_rates_land_lua),
            "ping_fail": await redis.script_load(ping_fail_lua),
            "freeze_rates": await redis.script_load(freeze_rates_lua),
            # "test": await redis.script_load('return tonumber(redis.call("GET", "nonexistent")) == nil'),
            # "test2": await redis.script_load('return nil or 2'),
        }

    async def get_sha(self, key: str):
        if self.shas is None:
            now = time()
            self.shas = await self.register_scripts()
            self.latency = time() - now
        return self.shas[key]

    async def get_token(self, server: str, method: str):
        app_prefix = f'{self.api_hash}:{self.game}:{server}'
        method_prefix = f'{self.api_hash}:{self.game}:{server}:{method}'
        redis = await self.redis.get()
        # print(await redis.evalsha(await self.get_sha("test2")))
        sha = await self.get_sha("get_token")
        now = time() + self.latency + 0.005
        # timeit = time()
        return_list: List[bytes] = await redis.evalsha(sha, [app_prefix, method_prefix], [str(now)])
        # print(time() - timeit)
        sleep = float(return_list[0].decode('utf-8'))
        allowed = return_list[1].decode('utf-8').split(";")[:-1]
        pinging_list = []
        for pinging in return_list[2].decode('utf-8').split(";")[:-1]:
            pings = pinging.split(",")[:-1]
            pings[-1] = int(pings[-1])
            pinging_list.append(pings)
        # print(return_list, allowed, pinging_list)
        return LimiterToken(server, method, now, sleep, allowed, pinging_list)

    async def sync_rates(self, token: LimiterToken, response: ClientResponse) -> Dict[str, List[List[int]]]:
        header = self.parse_headers(response)
        if header is None:
            await self.ping_fail(token)
            return
        redis = await self.redis.get()
        keys = []
        now = time() + self.latency + 0.005
        args = [str(now)]
        if token.pinging:
            for (prefix_i, type, i) in token.pinging:
                keys.append(prefix_i)
                if i >= len(header[f'{type}_limit']):
                    for _ in range(4):
                        args.append(0)
                else:
                    args.append(1)
                    args.append(header[f'{type}_limit'][i][0])
                    args.append(header[f'{type}_limit'][i][1])
                    args.append(header[f'{type}_count'][i][0])
            # print(args)
            sha = await self.get_sha("sync_rates.ping")
            await redis.evalsha(sha, keys, args)
        else:
            sha = await self.get_sha("sync_rates.land")
            await redis.evalsha(sha, token.allowed, [token.epoch])
        return header

    async def ping_fail(self, token: LimiterToken):
        redis = await self.redis.get()
        sha = await self.get_sha("ping_fail")
        await redis.evalsha(sha, [pinging[0] for pinging in token.pinging], [])

    async def freeze_rates(self, token: LimiterToken, response: ClientResponse) -> Dict[str, Union[str, int]]:
        header = self.parse_429(response)
        redis = await self.redis.get()
        sha = await self.get_sha("freeze_rates")
        now = time() + self.latency + 0.005
        args = [str(now), header["time"]]
        keys = []
        for (prefix_i, type, _) in token.pinging:
            if type != header["type"]:
                continue
            keys.append(prefix_i)
        await redis.evalsha(sha, keys, args)
        return header
