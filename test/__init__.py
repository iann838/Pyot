import pyot
import os

pyot.Settings(
    GAME_VARIANT = "LOL",
    DEFAULT_PLATFORM = "NA1",
    DEFAULT_REGION = "AMERICAS",
    PIPELINE = [
        {
            "BACKEND": "pyot.stores.Oden",
            "LOGS_ENABLED": True,
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