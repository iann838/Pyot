import aiohttp
from .objects import PtrCache

_utils_inner_cache = PtrCache()


async def _gather_summary(cache):
    url = "https://raw.communitydragon.org/pbe/plugins/rcp-be-lol-game-data/global/en_gb/v1/champion-summary.json"
    async with aiohttp.ClientSession() as session: # type: aiohttp.ClientSession
        response = await session.request("GET", url)
        if response and response.status == 200:
            dic = await response.json(encoding="utf-8")
            transformers = {
                "champion_id_by_key": {},
                "champion_id_by_name": {},
                "champion_key_by_id": {},
                "champion_key_by_name": {},
                "champion_name_by_id": {},
                "champion_name_by_key": {},
            }
            for champ in dic:
                if champ["id"] == -1:
                    continue
                transformers["champion_id_by_key"][champ["alias"]] = champ["id"]
                transformers["champion_id_by_name"][champ["name"]] = champ["id"]
                transformers["champion_key_by_id"][champ["id"]] = champ["alias"]
                transformers["champion_key_by_name"][champ["name"]] = champ["alias"]
                transformers["champion_name_by_id"][champ["id"]] = champ["name"]
                transformers["champion_name_by_key"][champ["alias"]] = champ["name"]
            for key, val in transformers.items():
                cache.set(key, val)


# IMPORTANT: _gather_summary() gathers all values, that's why it isn't passed as default.


async def champion_id_by_key(value):
    '''Convert champion key to id'''
    data = _utils_inner_cache.get("champion_id_by_key")
    if data is None:
        await _gather_summary(_utils_inner_cache)
        data = _utils_inner_cache.get("champion_id_by_key")
    return data[value]

async def champion_id_by_name(value):
    '''Convert champion name to id'''
    data = _utils_inner_cache.get("champion_id_by_name")
    if data is None:
        await _gather_summary(_utils_inner_cache)
        data = _utils_inner_cache.get("champion_id_by_name")
    return data[value]

async def champion_key_by_id(value):
    '''Convert champion id to key'''
    data = _utils_inner_cache.get("champion_key_by_id")
    if data is None:
        await _gather_summary(_utils_inner_cache)
        data = _utils_inner_cache.get("champion_key_by_id")
    return data[value]

async def champion_key_by_name(value):
    '''Convert champion name to key'''
    data = _utils_inner_cache.get("champion_key_by_name")
    if data is None:
        await _gather_summary(_utils_inner_cache)
        data = _utils_inner_cache.get("champion_key_by_name")
    return data[value]

async def champion_name_by_id(value):
    '''Convert champion id to name'''
    data = _utils_inner_cache.get("champion_name_by_id")
    if data is None:
        await _gather_summary(_utils_inner_cache)
        data = _utils_inner_cache.get("champion_name_by_id")
    return data[value]

async def champion_name_by_key(value):
    '''Convert champion key to name'''
    data = _utils_inner_cache.get("champion_name_by_key")
    if data is None:
        await _gather_summary(_utils_inner_cache)
        data = _utils_inner_cache.get("champion_name_by_key")
    return data[value]
