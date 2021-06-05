import aiohttp
from ..cache import PtrCache


_utils_inner_cache = PtrCache()


async def _gather_summary(cache):
    url = "https://raw.communitydragon.org/pbe/plugins/rcp-be-lol-game-data/global/en_gb/v1/champion-summary.json"
    async with aiohttp.ClientSession() as session: # type: aiohttp.ClientSession
        response = await session.request("GET", url)
        if response and response.status == 200:
            dic = await response.json(encoding="utf-8")
            transformers = {
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
                transformers["id_by_key"][champ["alias"]] = champ["id"]
                transformers["id_by_name"][champ["name"]] = champ["id"]
                transformers["key_by_id"][champ["id"]] = champ["alias"]
                transformers["key_by_name"][champ["name"]] = champ["alias"]
                transformers["name_by_id"][champ["id"]] = champ["name"]
                transformers["name_by_key"][champ["alias"]] = champ["name"]
            for key, val in transformers.items():
                cache.set(key, val)
        else:
            raise RuntimeError("Unable to pull champion summary")


# IMPORTANT: _gather_summary() gathers all values, that's why it isn't passed as default.


async def id_by_key(value):
    '''Convert champion key to id'''
    data = _utils_inner_cache.get("id_by_key")
    if data is None:
        await _gather_summary(_utils_inner_cache)
        data = _utils_inner_cache.get("id_by_key")
    return data[value]

async def id_by_name(value):
    '''Convert champion name to id'''
    data = _utils_inner_cache.get("id_by_name")
    if data is None:
        await _gather_summary(_utils_inner_cache)
        data = _utils_inner_cache.get("id_by_name")
    return data[value]

async def key_by_id(value):
    '''Convert champion id to key'''
    data = _utils_inner_cache.get("key_by_id")
    if data is None:
        await _gather_summary(_utils_inner_cache)
        data = _utils_inner_cache.get("key_by_id")
    return data[value]

async def key_by_name(value):
    '''Convert champion name to key'''
    data = _utils_inner_cache.get("key_by_name")
    if data is None:
        await _gather_summary(_utils_inner_cache)
        data = _utils_inner_cache.get("key_by_name")
    return data[value]

async def name_by_id(value):
    '''Convert champion id to name'''
    data = _utils_inner_cache.get("name_by_id")
    if data is None:
        await _gather_summary(_utils_inner_cache)
        data = _utils_inner_cache.get("name_by_id")
    return data[value]

async def name_by_key(value):
    '''Convert champion key to name'''
    data = _utils_inner_cache.get("name_by_key")
    if data is None:
        await _gather_summary(_utils_inner_cache)
        data = _utils_inner_cache.get("name_by_key")
    return data[value]
