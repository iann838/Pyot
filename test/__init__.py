from pyot.core import Settings
from pathlib import Path
import os


Settings(
    MODEL = "LOL",
    DEFAULT_PLATFORM = "NA1",
    DEFAULT_REGION = "AMERICAS",
    DEFAULT_LOCALE= "EN_US",
    PIPELINE = [
        {
            "BACKEND": "pyot.stores.Omnistone",
            "LOG_LEVEL": 30,
        },
        {
            "BACKEND": "pyot.stores.RedisCache",
            "LOG_LEVEL": 30,
            "DB": 1,
        },
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
                503: ("E", [3,3])
            }
        }
    ]
).activate()


Settings(
    MODEL = "TFT",
    DEFAULT_PLATFORM = "NA1",
    DEFAULT_REGION = "AMERICAS",
    DEFAULT_LOCALE= "EN_US",
    PIPELINE = [
        {
            "BACKEND": "pyot.stores.Omnistone",
            "LOG_LEVEL": 30,
        },
        {
            "BACKEND": "pyot.stores.DiskCache",
            "LOG_LEVEL": 30,
            "DIRECTORY": Path.cwd() / 'diskcache',
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
            "API_KEY": "RGAPI-5d51ad95-e77c-4f30-987a-bc0db2a*****", # <--- HEY CRACK THIS KEY
            "RATE_LIMITER": {
                "BACKEND": "pyot.limiters.MemoryLimiter",
                "LIMITING_SHARE": 1,
            },
            "ERROR_HANDLING": {
                400: ("T", []),
                503: ("E", [3,3])
            }
        }
    ]
).activate()


Settings(
    MODEL = "VAL",
    DEFAULT_PLATFORM = "NA",
    DEFAULT_REGION = "AMERICAS",
    DEFAULT_LOCALE= "EN-US",
    PIPELINE = [
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
                503: ("E", [3,3])
            }
        }
    ]
).activate()
