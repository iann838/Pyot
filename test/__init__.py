import platform
import os

from pyot.core import Settings

# Fix: Windows `asyncio.run()` will throw `RuntimeError: Event loop is closed`.
# Refer: https://github.com/aio-libs/aiohttp/issues/4324

if platform.system() == 'Windows':
    from pyot.utils.internal import silence_proactor_pipe_deallocation
    silence_proactor_pipe_deallocation()


Settings(
    MODEL="LOL",
    DEFAULT_PLATFORM="NA1",
    DEFAULT_REGION="AMERICAS",
    DEFAULT_LOCALE="EN_US",
    PIPELINE=[
        {
            "BACKEND": "pyot.stores.Omnistone",
            "LOG_LEVEL": 30,
            "EXPIRATIONS": {
                "summoner_v4_by_name": 100,
                "match_v4_match": 600,
                "match_v4_timeline": 600,
            }
        },
        # {
        #     "BACKEND": "pyot.stores.RedisCache",
        #     "LOG_LEVEL": 30,
        #     "DB": 1,
        #     "EXPIRATIONS": {
        #         "match_v4_match": 600,
        #         "match_v4_timeline": 600,
        #     }
        # },
        {
            "BACKEND": "pyot.stores.MerakiCDN",
            "LOG_LEVEL": 30,
            "ERROR_HANDLING": {
                404: ("T", []),
                500: ("R", [3])
            }
        },
        {
            "BACKEND": "pyot.stores.CDragon",
            "LOG_LEVEL": 30,
            "ERROR_HANDLING": {
                404: ("T", []),
                500: ("R", [3])
            }
        },
        {
            "BACKEND": "pyot.stores.RiotAPI",
            "LOG_LEVEL": 30,
            "API_KEY": os.environ["RIOT_API_KEY"],
            "RATE_LIMITER": {
                "BACKEND": "pyot.limiters.RedisLimiter",
                "LIMITING_SHARE": 1,
                "HOST": "127.0.0.1",
                "PORT": 6379,
                "DB": 0,
            },
            "ERROR_HANDLING": {
                400: ("T", []),
                503: ("E", [3, 3])
            }
        }
    ]
).activate()


Settings(
    MODEL="LOR",
    DEFAULT_REGION="AMERICAS",
    DEFAULT_LOCALE="EN_US",
    PIPELINE=[
        {
            "BACKEND": "pyot.stores.Omnistone",
            "LOG_LEVEL": 30,
            "EXPIRATIONS": {
                "match_v1_match": 10
            }
        },
        {
            "BACKEND": "pyot.stores.DDragon",
            "LOG_LEVEL": 30,
            "ERROR_HANDLING": {
                404: ("T", []),
                500: ("R", [3])
            }
        },
        {
            "BACKEND": "pyot.stores.RiotAPI",
            "API_KEY": os.environ["LOR_API_KEY"],
            "LOG_LEVEL": 30,
            "RATE_LIMITER": {
                "BACKEND": "pyot.limiters.MemoryLimiter",
                "LIMITING_SHARE": 1,
            },
            "ERROR_HANDLING": {
                400: ("T", []),
                503: ("E", [3, 3])
            }
        }
    ]
).activate()


Settings(
    MODEL="TFT",
    DEFAULT_PLATFORM="NA1",
    DEFAULT_REGION="AMERICAS",
    DEFAULT_LOCALE="EN_US",
    PIPELINE=[
        {
            "BACKEND": "pyot.stores.Omnistone",
            "LOG_LEVEL": 30,
        },
        {
            "BACKEND": "pyot.stores.CDragon",
            "LOG_LEVEL": 30,
            "ERROR_HANDLING": {
                404: ("T", []),
                500: ("R", [3])
            }
        },
        {
            "BACKEND": "pyot.stores.RiotAPI",
            "API_KEY": os.environ["TFT_API_KEY"],
            "RATE_LIMITER": {
                "BACKEND": "pyot.limiters.MemoryLimiter",
                "LIMITING_SHARE": 1,
            },
            "ERROR_HANDLING": {
                400: ("T", []),
                503: ("E", [3, 3])
            }
        }
    ]
).activate()


Settings(
    MODEL="VAL",
    DEFAULT_PLATFORM="NA",
    DEFAULT_REGION="AMERICAS",
    DEFAULT_LOCALE="EN-US",
    PIPELINE=[
        {
            "BACKEND": "pyot.stores.Omnistone",
            "LOG_LEVEL": 30,
        },
        {
            "BACKEND": "pyot.stores.RiotAPI",
            "API_KEY": os.environ["VALORANT_DEV_KEY"],
            "RATE_LIMITER": {
                "BACKEND": "pyot.limiters.MemoryLimiter",
                "LIMITING_SHARE": 1,
            },
            "ERROR_HANDLING": {
                400: ("T", []),
                503: ("E", [3, 3])
            }
        }
    ]
).activate()
