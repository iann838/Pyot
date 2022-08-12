import asyncio
import contextlib
from datetime import datetime, timedelta

from ..aiohttp import SafeClientSession
from ..functools import async_property


class ChampionKeysCache:

    def __init__(self) -> None:
        self._is_locked = False
        self.cached_data = {
            "id_by_key": {},
            "id_by_name": {},
            "key_by_id": {},
            "key_by_name": {},
            "name_by_id": {},
            "name_by_key": {},
        }
        self.last_updated = datetime.now() - timedelta(days=1)

    def __str__(self) -> str:
        return 'ChampionKeysCache()'

    @property
    @contextlib.asynccontextmanager
    async def _lock(self):
        try:
            while self._is_locked:
                await asyncio.sleep(0.01)
            self._is_locked = True
            yield None
        finally:
            self._is_locked = False

    @async_property
    async def data(self):
        if datetime.now() - self.last_updated < timedelta(hours=3):
            return self.cached_data
        async with self._lock:
            if datetime.now() - self.last_updated < timedelta(hours=3):
                return self.cached_data
            url = "https://raw.communitydragon.org/pbe/plugins/rcp-be-lol-game-data/global/en_gb/v1/champion-summary.json"
            async with SafeClientSession() as session:
                response = await session.get(url)
                if not (response and response.status == 200):
                    raise RuntimeError(f"Failed to pull champion summary ({response.status})")
                dic = await response.json(encoding="utf-8")
            data = {
                "id_by_key": {},
                "id_by_name": {},
                "key_by_id": {},
                "key_by_name": {},
                "name_by_id": {},
                "name_by_key": {},
            }
            for champ in dic:
                if champ["id"] == -1:
                    continue
                data["id_by_key"][champ["alias"]] = champ["id"]
                data["id_by_name"][champ["name"]] = champ["id"]
                data["key_by_id"][champ["id"]] = champ["alias"]
                data["key_by_name"][champ["name"]] = champ["alias"]
                data["name_by_id"][champ["id"]] = champ["name"]
                data["name_by_key"][champ["alias"]] = champ["name"]
            self.cached_data = data
            self.last_updated = datetime.now()
        return self.cached_data


champion_keys_cache = ChampionKeysCache()


async def id_by_key(value: str) -> int:
    '''Get champion id by key'''
    data = await champion_keys_cache.data
    return data["id_by_key"][value]


async def id_by_name(value: str) -> int:
    '''Get champion id by name'''
    data = await champion_keys_cache.data
    return data["id_by_name"][value]


async def key_by_id(value: int) -> str:
    '''Get champion key by id'''
    data = await champion_keys_cache.data
    return data["key_by_id"][value]


async def key_by_name(value: str) -> str:
    '''Get champion key by name'''
    data = await champion_keys_cache.data
    return data["key_by_name"][value]


async def name_by_id(value: int) -> str:
    '''Get champion name by id'''
    data = await champion_keys_cache.data
    return data["name_by_id"][value]


async def name_by_key(value: str) -> str:
    '''Get champion name by key'''
    data = await champion_keys_cache.data
    return data["name_by_key"][value]
