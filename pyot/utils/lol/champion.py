import aiohttp
from ..cache import PtrCache


CHAMPION_SUMMARY = PtrCache()


async def fill_champion_summary(cache: PtrCache):
    '''Fill champion summary data to cache.'''
    url = "https://raw.communitydragon.org/pbe/plugins/rcp-be-lol-game-data/global/en_gb/v1/champion-summary.json"
    async with aiohttp.ClientSession() as session:
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


async def id_by_key(value):
    '''Get champion id by key'''
    data = CHAMPION_SUMMARY.get("id_by_key")
    if data is None:
        await fill_champion_summary(CHAMPION_SUMMARY)
        data = CHAMPION_SUMMARY.get("id_by_key")
    return data[value]


async def id_by_name(value):
    '''Get champion id by name'''
    data = CHAMPION_SUMMARY.get("id_by_name")
    if data is None:
        await fill_champion_summary(CHAMPION_SUMMARY)
        data = CHAMPION_SUMMARY.get("id_by_name")
    return data[value]


async def key_by_id(value):
    '''Get champion key by id'''
    data = CHAMPION_SUMMARY.get("key_by_id")
    if data is None:
        await fill_champion_summary(CHAMPION_SUMMARY)
        data = CHAMPION_SUMMARY.get("key_by_id")
    return data[value]


async def key_by_name(value):
    '''Get champion key by name'''
    data = CHAMPION_SUMMARY.get("key_by_name")
    if data is None:
        await fill_champion_summary(CHAMPION_SUMMARY)
        data = CHAMPION_SUMMARY.get("key_by_name")
    return data[value]


async def name_by_id(value):
    '''Get champion name by id'''
    data = CHAMPION_SUMMARY.get("name_by_id")
    if data is None:
        await fill_champion_summary(CHAMPION_SUMMARY)
        data = CHAMPION_SUMMARY.get("name_by_id")
    return data[value]


async def name_by_key(value):
    '''Get champion name by key'''
    data = CHAMPION_SUMMARY.get("name_by_key")
    if data is None:
        await fill_champion_summary(CHAMPION_SUMMARY)
        data = CHAMPION_SUMMARY.get("name_by_key")
    return data[value]
