import pyot
import os
import aiohttp
from datetime import timedelta as td


pyot.Settings(
    MODEL = "LOL",
    GATHERER = {
        "LOGS_ENABLED": True,
        "SESSION_CLASS": aiohttp.ClientSession,
        "CANCEL_ON_RAISE": False,
    },
    DEFAULT_PLATFORM = "NA1",
    DEFAULT_REGION = "AMERICAS",
    DEFAULT_LOCALE= "EN_US",
    PIPELINE = [
        {
            "BACKEND": "pyot.stores.Omnistone",
            "EXPIRATIONS": {
                "summoner_v4_by_name": 0,
                "league_v4_challenger_league": td(minutes=10),
            }
        },
        {
            "BACKEND": "pyot.stores.DjangoCache",
            "ALIAS": "pyot-redis",
            "EXPIRATIONS": {
                "summoner_v4_by_name": td(seconds=10),
                "*": 0
            }
        },
        {
            "BACKEND": "pyot.stores.MerakiCDN",
            "LOGS_ENABLED": True,
            "ERROR_HANDLING": {
                404: ("T", []),
                500: ("R", [3])
            }
        },
        {
            "BACKEND": "pyot.stores.CDragon",
            "LOGS_ENABLED": True,
            "ERROR_HANDLING": {
                404: ("T", []),
                500: ("R", [3])
            }
        },
        {
            "BACKEND": "pyot.stores.RiotAPI",
            "KEY": os.environ["RIOT_API_KEY"],
            "LIMITING_SHARE": 1,
            "ERROR_HANDLING": {
                400: ("T", []),
                503: ("E", [3,3])
            }
        }
    ]
).activate()


pyot.Settings(
    MODEL = "VAL",
    GATHERER = {
        "LOGS_ENABLED": True,
        "SESSION_CLASS": aiohttp.ClientSession,
        "CANCEL_ON_RAISE": False,
    },
    DEFAULT_PLATFORM = "NA",
    DEFAULT_REGION = "AMERICAS",
    DEFAULT_LOCALE= "EN-US",
    PIPELINE = [
        {
            "BACKEND": "pyot.stores.Omnistone",
            "LOGS_ENABLED": False,
        },
        {
            "BACKEND": "pyot.stores.RiotAPI",
            "KEY": os.environ["VALORANT_DEV_KEY"],
            "LIMITING_SHARE": 1,
            "ERROR_HANDLING": {
                400: ("T", []),
                503: ("E", [3,3])
            }
        }
    ]
).activate()