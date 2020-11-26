# Default settings for pyot projects.
# Change these settings according to your needs.

import platform
import os


# Fix: Windows `asyncio.run()` will throw `RuntimeError: Event loop is closed`.
# Refer: https://github.com/aio-libs/aiohttp/issues/4324

if platform.system() == 'Windows':
    from asyncio.proactor_events import _ProactorBasePipeTransport
    from pyot.utils.internal import silence_event_loop_closed
    _ProactorBasePipeTransport.__del__ = silence_event_loop_closed(_ProactorBasePipeTransport.__del__)


# Pyot documentations for settings
# https://paaksing.github.io/Pyot/core/settings.html

# Pyot documentations for pipeline stores
# https://paaksing.github.io/Pyot/stores/

from pyot.core import Settings


Settings(
    MODEL = "LOL",
    DEFAULT_PLATFORM = "NA1",
    DEFAULT_REGION = "AMERICAS",
    DEFAULT_LOCALE= "EN_US",
    PIPELINE = [
        {"BACKEND": "pyot.stores.Omnistone"},
        {"BACKEND": "pyot.stores.MerakiCDN"},
        {"BACKEND": "pyot.stores.CDragon"},
        {
            "BACKEND": "pyot.stores.RiotAPI",
            "API_KEY": os.environ["RIOT_API_KEY"], # API KEY
        }
    ]
).activate() # <- DON'T FORGET TO ACTIVATE THE SETTINGS
