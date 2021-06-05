# Default settings for pyot projects.
# Change these settings according to your needs.

import os
import platform

from pyot.core.settings import AppConf, ModelConf, PipelineDef


# Fix: Windows `asyncio.run()` will throw `RuntimeError: Event loop is closed`.
# Refer: https://github.com/aio-libs/aiohttp/issues/4324

if platform.system() == 'Windows':
    from pyot.utils.internal import silence_proactor_pipe_deallocation
    silence_proactor_pipe_deallocation()


# Pyot documentations for settings
# https://paaksing.github.io/Pyot/core/settings.html

# Pyot documentations for pipeline stores
# https://paaksing.github.io/Pyot/stores/


AppConf(
    # Used for projects generated with `pyot startproject`
    CLOUDLINE_URL="/cloudline",
    OPENAPI_URL="/openapi",
    SERVER_PORT=8000,
).activate()


ModelConf(
    MODEL="LOL",
    DEFAULT_PLATFORM="NA1",
    DEFAULT_REGION="AMERICAS",
    DEFAULT_LOCALE="EN_US",
).activate()


PipelineDef(
    MODEL="LOL",
    NAME="main",
    DEFAULT=True,
    PIPELINE=[
        {"BACKEND": "pyot.stores.omnistone.Omnistone"},
        {"BACKEND": "pyot.stores.merakicdn.MerakiCDN"},
        {"BACKEND": "pyot.stores.cdragon.CDragon"},
        {
            "BACKEND": "pyot.stores.riotapi.RiotAPI",
            "API_KEY": os.environ["RIOT_API_KEY"], # API KEY
        }
    ]
).activate()
